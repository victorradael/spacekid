'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const { scaffold } = require('../src');

function tmpDir() {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'spacekid-'));
}

const read = (...parts) => fs.readFileSync(path.join(...parts), 'utf8');

test('fresh project creates all three files with name from package.json', () => {
  const dir = tmpDir();
  fs.writeFileSync(path.join(dir, 'package.json'), JSON.stringify({ name: 'widgets' }));

  const results = scaffold(dir);

  assert.deepEqual(results.map((r) => r.status), ['created', 'created', 'created']);
  assert.match(read(dir, 'AGENTS.md'), /Agent Guide — widgets/);
  assert.ok(fs.existsSync(path.join(dir, 'specs', 'AGENTS.md')));
  assert.ok(fs.existsSync(path.join(dir, 'plans', 'AGENTS.md')));
});

test('falls back to the directory name without package.json', () => {
  const dir = path.join(tmpDir(), 'my-project');
  fs.mkdirSync(dir);

  scaffold(dir);

  assert.match(read(dir, 'AGENTS.md'), /Agent Guide — my-project/);
});

test('malformed package.json falls back to the directory name', () => {
  const dir = path.join(tmpDir(), 'fallback');
  fs.mkdirSync(dir);
  fs.writeFileSync(path.join(dir, 'package.json'), '{ not json');

  scaffold(dir);

  assert.match(read(dir, 'AGENTS.md'), /Agent Guide — fallback/);
});

test('explicit name overrides detection', () => {
  const dir = tmpDir();
  fs.writeFileSync(path.join(dir, 'package.json'), JSON.stringify({ name: 'widgets' }));

  scaffold(dir, 'override');

  assert.match(read(dir, 'AGENTS.md'), /Agent Guide — override/);
});

test('existing root AGENTS.md is left untouched and reported skipped', () => {
  const dir = tmpDir();
  const existing = '# My own AGENTS.md\n\ncustom content\n';
  fs.writeFileSync(path.join(dir, 'AGENTS.md'), existing);

  const results = scaffold(dir);

  assert.equal(results[0].status, 'skipped');
  assert.equal(read(dir, 'AGENTS.md'), existing);
});

test('existing specs/plans AGENTS.md are preserved and appended to', () => {
  const dir = tmpDir();
  fs.mkdirSync(path.join(dir, 'specs'));
  fs.mkdirSync(path.join(dir, 'plans'));
  const existingSpecs = '# Our own spec rules\n\ndo it our way\n';
  const existingPlans = '# Our own plan rules\n\ndo it our way\n';
  fs.writeFileSync(path.join(dir, 'specs', 'AGENTS.md'), existingSpecs);
  fs.writeFileSync(path.join(dir, 'plans', 'AGENTS.md'), existingPlans);

  const results = scaffold(dir);

  assert.equal(results[1].status, 'appended');
  assert.equal(results[2].status, 'appended');
  const specs = read(dir, 'specs', 'AGENTS.md');
  const plans = read(dir, 'plans', 'AGENTS.md');
  assert.ok(specs.startsWith(existingSpecs));
  assert.ok(plans.startsWith(existingPlans));
  assert.ok(specs.length > existingSpecs.length);
  assert.ok(plans.length > existingPlans.length);
});

test('missing specs/ and plans/ directories are created', () => {
  const dir = tmpDir();

  scaffold(dir);

  assert.ok(fs.statSync(path.join(dir, 'specs')).isDirectory());
  assert.ok(fs.statSync(path.join(dir, 'plans')).isDirectory());
});

test('running scaffold twice does not corrupt files', () => {
  const dir = tmpDir();
  scaffold(dir);
  const rootAfterFirst = read(dir, 'AGENTS.md');
  const specsAfterFirst = read(dir, 'specs', 'AGENTS.md');

  const results = scaffold(dir);

  assert.deepEqual(results.map((r) => r.status), ['skipped', 'appended', 'appended']);
  assert.equal(read(dir, 'AGENTS.md'), rootAfterFirst);
  assert.ok(read(dir, 'specs', 'AGENTS.md').startsWith(specsAfterFirst));
});
