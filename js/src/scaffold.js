'use strict';

const fs = require('node:fs');
const path = require('node:path');

const APP_NAME_PLACEHOLDER = '{{APP_NAME}}';
const TEMPLATES_DIR = path.join(__dirname, 'templates');

function loadTemplate(filename) {
  return fs.readFileSync(path.join(TEMPLATES_DIR, filename), 'utf8');
}

function detectAppName(projectRoot) {
  const manifest = path.join(projectRoot, 'package.json');
  if (fs.existsSync(manifest)) {
    try {
      const { name } = JSON.parse(fs.readFileSync(manifest, 'utf8'));
      if (typeof name === 'string' && name.length > 0) {
        return name;
      }
    } catch {
      // Unreadable or malformed package.json: fall back to the directory name.
    }
  }
  return path.basename(path.resolve(projectRoot));
}

function renderRootAgents(appName) {
  return loadTemplate('root-agents.md').split(APP_NAME_PLACEHOLDER).join(appName);
}

function writeOrSkip(filePath, content) {
  if (fs.existsSync(filePath)) {
    return { path: filePath, status: 'skipped' };
  }
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, content, 'utf8');
  return { path: filePath, status: 'created' };
}

function writeOrAppend(filePath, content) {
  if (fs.existsSync(filePath)) {
    fs.appendFileSync(filePath, '\n' + content, 'utf8');
    return { path: filePath, status: 'appended' };
  }
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, content, 'utf8');
  return { path: filePath, status: 'created' };
}

function scaffold(projectRoot, appName) {
  const root = path.resolve(projectRoot);
  const resolvedName = appName || detectAppName(root);

  return [
    writeOrSkip(path.join(root, 'AGENTS.md'), renderRootAgents(resolvedName)),
    writeOrAppend(path.join(root, 'specs', 'AGENTS.md'), loadTemplate('specs-agents.md')),
    writeOrAppend(path.join(root, 'plans', 'AGENTS.md'), loadTemplate('plans-agents.md')),
  ];
}

module.exports = {
  detectAppName,
  renderRootAgents,
  writeOrSkip,
  writeOrAppend,
  scaffold,
};
