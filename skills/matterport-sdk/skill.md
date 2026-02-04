# Matterport SDK Specialist

## Domain Expertise

- Matterport SDK (Showcase SDK, Embed SDK)
- Viewer integration and lifecycle management
- 3D space data formats and structures (camera poses, mattertags, sweeps)
- SDK event handling and subscriptions
- Camera control and navigation
- Scene graph manipulation

## Responsibilities

1. **Implement SDK Integrations** following established patterns
2. **Handle Viewer Lifecycle** (initialization, ready state, cleanup)
3. **Work with SDK Data Formats** (poses, mattertags, sweeps, floors)
4. **Establish SDK Usage Patterns** and best practices
5. **Update Knowledge Base** with SDK patterns and gotchas

## Pre-Flight Checks

Before implementing, ALWAYS:

1. **Read KB Patterns**: Check `kb/matterport-integration.md` for existing SDK patterns
2. **Read Design Docs**: Get specifications from workspace design documents
3. **Read Frontend Patterns**: Check `kb/frontend-patterns.md` for service patterns
4. **Check SDK Version**: Verify which Matterport SDK version is in use

```bash
cat kb/matterport-integration.md 2>/dev/null || echo "No SDK patterns documented yet"
cat kb/frontend-patterns.md
cat work/*-design.md 2>/dev/null || true
```

## Task Execution Steps

### 1. Review Integration Requirements

Read design specifications:
- SDK features needed (Camera, Sweep, Mattertag, etc.)
- Event subscriptions required
- Data structures to work with
- Lifecycle requirements

### 2. Implement SDK Integration

Follow established patterns:
- Use async/await for SDK initialization
- Subscribe to relevant SDK events
- Handle SDK data formats correctly
- Add error handling for SDK failures

### 3. Handle Viewer Lifecycle

Ensure proper lifecycle management:
- Wait for viewer ready state
- Clean up subscriptions on teardown
- Handle viewer reconnection if needed

### 4. Document SDK Patterns

Update knowledge base:
- Add new SDK usage patterns to `kb/matterport-integration.md`
- Document SDK quirks or gotchas encountered
- Note SDK version compatibility issues

## Post-Work Updates

After implementation, update:

1. **kb/matterport-integration.md**: Add new SDK patterns and usage examples
2. **Design Document**: Add implementation notes and file paths
3. **Work Notes**: Document SDK quirks, version issues, or workarounds

```bash
echo "## SDK Pattern: <feature>" >> kb/matterport-integration.md
echo "<implementation details>" >> kb/matterport-integration.md
```

## System Prompt

```
You are a Matterport SDK Specialist implementing 3D viewer integrations.

WORKFLOW:

1. PRE-FLIGHT CHECKS (REQUIRED):
   - Read kb/matterport-integration.md for existing SDK patterns
   - Read design requirements from workspace documents
   - Read kb/frontend-patterns.md for service patterns
   - Check Matterport SDK version in use

2. IMPLEMENTATION:
   - Initialize Matterport viewer following lifecycle pattern
   - Subscribe to SDK events (Camera.pose, Sweep.current, etc.)
   - Work with SDK data formats (poses, mattertags, sweeps)
   - Add error handling for SDK connection/subscription failures
   - Clean up SDK resources on teardown

3. KNOWLEDGE BASE UPDATES (REQUIRED):
   - Update kb/matterport-integration.md with new SDK patterns
   - Document SDK quirks or version-specific behaviors
   - Add implementation notes to design doc

CONSTRAINTS:
- ALWAYS read KB patterns before implementing
- ALWAYS use async/await for SDK operations
- ALWAYS handle SDK initialization failures gracefully
- ALWAYS clean up SDK subscriptions on teardown
- ALWAYS update KB after implementation

Current task: {task_description}
Design document: {design_doc_path}
```

## SDK Integration Pattern

### Complete Initialization Example

```javascript
/**
 * Matterport viewer lifecycle pattern
 * Based on BlackBox production implementation
 */

class MatterportService {
  constructor() {
    this.sdk = null;
    this.subscriptions = [];
  }

  /**
   * Initialize Matterport SDK and subscribe to events
   * @param {string} modelId - Matterport model ID
   * @returns {Promise<SDK>} Initialized SDK instance
   */
  async init(modelId) {
    const viewer = document.querySelector('#mpv');
    if (!viewer) throw new Error('Matterport viewer element not found');

    // Wait for custom element to be defined
    await customElements.whenDefined('matterport-viewer');

    // Connect to SDK (self-hosted bundle pattern)
    this.sdk = await viewer.playingPromise;

    // Subscribe to SDK events
    await this._subscribeToEvents();

    // Build sweep graph for navigation
    await this._buildSweepGraph();

    return this.sdk;
  }

  /**
   * Subscribe to SDK events with error handling
   */
  async _subscribeToEvents() {
    // Camera pose subscription
    try {
      const poseSub = this.sdk.Camera.pose.subscribe(pose => {
        // Handle pose updates
        if (pose?.sweep) {
          this.currentSweepId = pose.sweep;
        }
      });
      this.subscriptions.push(poseSub);
    } catch (e) {
      console.warn('Camera pose subscription failed:', e);
    }

    // Current sweep subscription
    try {
      const sweepSub = this.sdk.Sweep.current.subscribe(sweep => {
        if (sweep?.sid) {
          this.onSweepChanged(sweep.sid);
        }
      });
      this.subscriptions.push(sweepSub);
    } catch (e) {
      console.warn('Sweep subscription failed:', e);
    }

    // Floor subscription
    try {
      const floorSub = this.sdk.Floor.current.subscribe(floor => {
        this.onFloorChanged(floor);
      });
      this.subscriptions.push(floorSub);
    } catch (e) {
      console.warn('Floor subscription failed:', e);
    }
  }

  /**
   * Build sweep graph for pathfinding
   */
  async _buildSweepGraph() {
    // Wait for sweep data to stabilize
    await new Promise(async (resolve, reject) => {
      const timeout = setTimeout(() => reject(new Error('Sweep data timeout')), 15000);

      try {
        const modelData = await this.sdk.Model.getData();
        if (modelData?.sweeps?.length > 0) {
          clearTimeout(timeout);
          resolve();
          return;
        }
      } catch {}

      // Subscribe to sweep data updates
      let stabilityTimer = null;
      const unsub = this.sdk.Sweep.data.subscribe({
        onAdded() {
          if (stabilityTimer) clearTimeout(stabilityTimer);
          stabilityTimer = setTimeout(() => {
            try { unsub(); } catch {}
            clearTimeout(timeout);
            resolve();
          }, 500);
        }
      });
    });

    // Fetch sweep data and build adjacency graph
    const sweepData = await this.sdk.Sweep.data.getData();
    this.sweepGraph = this._buildAdjacencyGraph(sweepData);
  }

  /**
   * Clean up SDK resources
   */
  cleanup() {
    // Unsubscribe from all SDK events
    this.subscriptions.forEach(sub => {
      try { sub(); } catch {}
    });
    this.subscriptions = [];

    // Disconnect from SDK
    if (this.sdk) {
      try { this.sdk.disconnect(); } catch {}
      this.sdk = null;
    }
  }

  /**
   * Move camera to specific pose
   * @param {Object} pose - Camera pose {position, rotation, projection, sweep}
   */
  async moveToPose(pose) {
    if (!this.sdk) throw new Error('SDK not initialized');

    await this.sdk.Camera.pose.moveTo({
      position: pose.position,
      rotation: pose.rotation,
      projection: pose.projection || this.sdk.Camera.Projection.PERSPECTIVE,
      sweep: pose.sweep,
      transition: this.sdk.Camera.Transition.FLY,
      speed: 1.0
    });
  }

  /**
   * Add mattertag to scene
   * @param {Object} tag - Mattertag data
   */
  async addMattertag(tag) {
    if (!this.sdk) throw new Error('SDK not initialized');

    const [sid] = await this.sdk.Mattertag.add([{
      label: tag.label,
      description: tag.description || '',
      anchorPosition: tag.position,
      stemVector: tag.stemVector || { x: 0, y: 0.3, z: 0 },
      color: tag.color || { r: 1, g: 0, b: 0 }
    }]);

    return sid;
  }
}
```

### Alternative Pattern: MP_SDK.connect()

For standard Matterport embed (non-self-hosted):

```javascript
/**
 * Initialize SDK using MP_SDK.connect()
 * Standard pattern for hosted Matterport iframes
 */
async function initMatterport(modelId) {
  const iframe = document.getElementById('matterport-viewer');

  // Connect to SDK in iframe
  const sdk = await window.MP_SDK.connect(iframe, {
    applicationKey: 'YOUR_SDK_KEY'
  });

  // Configure model
  await sdk.Scene.configure({
    modelId: modelId
  });

  // Wait for viewer ready
  await new Promise((resolve) => {
    sdk.on('viewer.ready', () => {
      console.log('Matterport viewer ready');
      resolve();
    });
  });

  return sdk;
}

/**
 * Cleanup SDK connection
 */
function cleanupMatterport(sdk) {
  if (sdk) {
    try {
      sdk.disconnect();
    } catch (e) {
      console.warn('SDK disconnect failed:', e);
    }
  }
}
```

### Common SDK Data Formats

#### Camera Pose
```javascript
{
  position: { x: 1.5, y: 1.2, z: -3.4 },
  rotation: { x: 0.1, y: 2.3, z: 0.0 },
  projection: sdk.Camera.Projection.PERSPECTIVE,
  sweep: "sweepId123"
}
```

#### Sweep Data
```javascript
{
  sid: "sweepId123",
  uuid: "uuid-string",
  position: { x: 1.5, y: 0.0, z: -3.4 },
  neighbors: ["sweepId456", "sweepId789"],
  floorInfo: { sequence: 0 }
}
```

#### Mattertag
```javascript
{
  sid: "tagId123",
  label: "Equipment Name",
  description: "Equipment details",
  anchorPosition: { x: 1.5, y: 1.2, z: -3.4 },
  stemVector: { x: 0, y: 0.3, z: 0 },
  color: { r: 1, g: 0, b: 0 }
}
```

## Common SDK Patterns

### Wait for Data Stability

SDK data may load asynchronously. Use subscription pattern:

```javascript
async function waitForSweeps(sdk) {
  return new Promise((resolve, reject) => {
    const timeout = setTimeout(() => reject(new Error('Timeout')), 15000);

    let stabilityTimer = null;
    const unsub = sdk.Sweep.data.subscribe({
      onAdded() {
        if (stabilityTimer) clearTimeout(stabilityTimer);
        stabilityTimer = setTimeout(() => {
          unsub();
          clearTimeout(timeout);
          resolve();
        }, 500);
      }
    });
  });
}
```

### Handle SDK Errors

Always wrap SDK calls in try/catch:

```javascript
try {
  const subscription = sdk.Camera.pose.subscribe(pose => {
    // Handle pose
  });
} catch (e) {
  console.warn('Subscription failed:', e);
  // Fallback behavior
}
```

### Register Custom Components

For rendering custom scene objects:

```javascript
async function registerComponent(sdk, componentName, componentClass) {
  const [sceneObject] = await sdk.Scene.createObjects(1);
  const node = sceneObject.addNode();
  const component = node.addComponent(componentName);

  await component.bind(componentClass);
  await component.waitUntilBound();

  return { sceneObject, node, component };
}
```

## SDK Gotchas and Best Practices

### 1. Subscription Cleanup
Always store and clean up subscriptions to prevent memory leaks:
```javascript
this.subscriptions.push(sdk.Camera.pose.subscribe(...));
// Later:
this.subscriptions.forEach(unsub => unsub());
```

### 2. Data Race Conditions
Wait for data stability before using sweep/mattertag data:
- Use subscription patterns with stability timers
- Don't assume data is available immediately after SDK init

### 3. Custom Element Lifecycle
For self-hosted SDK, wait for custom element:
```javascript
await customElements.whenDefined('matterport-viewer');
```

### 4. Error Handling
SDK subscriptions can fail - always add try/catch and fallbacks

### 5. Scene Object Lifecycle
Scene objects must be explicitly started:
```javascript
sceneObject.start();
```

## Output Deliverables

- SDK integration code following lifecycle pattern
- Event subscription handlers with error handling
- Data format parsers/validators
- KB updates with new SDK patterns
- Workspace notes documenting SDK quirks or gotchas
