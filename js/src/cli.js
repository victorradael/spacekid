'use strict';

const path = require('node:path');
const { parseArgs } = require('node:util');

const { scaffold } = require('./scaffold');

const STATUS_LABEL = {
  created: 'created',
  appended: 'appended to',
  skipped: 'skipped (already exists)',
};

const USAGE = `usage: spacekid init [--path <dir>] [--name <name>]

  init    scaffold the SpaceKid AGENTS.md cycle in a project
`;

function init(args) {
  const { values } = parseArgs({
    args,
    options: {
      path: { type: 'string', default: '.' },
      name: { type: 'string' },
    },
    allowPositionals: false,
  });

  const projectRoot = path.resolve(values.path);
  for (const result of scaffold(projectRoot, values.name)) {
    console.log(`${STATUS_LABEL[result.status]}: ${path.relative(projectRoot, result.path)}`);
  }
  return 0;
}

function main(argv) {
  const [command, ...rest] = argv;
  if (command !== 'init') {
    process.stderr.write(USAGE);
    return 1;
  }
  try {
    return init(rest);
  } catch (err) {
    process.stderr.write(`spacekid: ${err.message}\n${USAGE}`);
    return 1;
  }
}

module.exports = { main };
