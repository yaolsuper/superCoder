/**
 * superCoder OpenCode harness scaffold.
 *
 * The core superCoder Skill Pack is harness-neutral. This file documents the
 * expected adapter boundary without mutating user global configuration.
 */

const path = require("path");

function createSuperCoderPlugin() {
  const root = path.resolve(__dirname, "../..");

  return {
    name: "supercoder-opencode-harness",
    version: "0.1.0",
    skillsDir: path.join(root, "skills"),
    entrySkill: "superCoder",
    toolMapping: path.join(__dirname, "tool-mapping.md"),
  };
}

module.exports = createSuperCoderPlugin;
