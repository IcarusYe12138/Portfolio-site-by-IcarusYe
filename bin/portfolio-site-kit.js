#!/usr/bin/env node
/**
 * portfolio-site-kit — installer
 *
 * Copies the skill (SKILL.md + references/ + templates/ + tools/ + examples/)
 * into your agent's skills directory. Zero dependencies.
 *
 * Usage:
 *   npx portfolio-site-kit                # auto-detect skills dir, install
 *   portfolio-site-kit --dir <path>       # explicit target directory
 *   portfolio-site-kit --force            # overwrite an existing install
 */
'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const readline = require('readline');

const SKILL_NAME = 'portfolio-site-kit';
const ASSETS = ['SKILL.md', 'references', 'templates', 'tools', 'examples'];

// Candidate skills directories: [agent label, dir under home]
const CANDIDATES = [
  ['TRAE (CN)', '.trae-cn/skills'],
  ['TRAE', '.trae/skills'],
  ['Claude Code', '.claude/skills'],
  ['Codex', '.codex/skills'],
  ['Cursor', '.cursor/skills'],
  ['OpenCode', '.config/opencode/skills'],
];

function parseArgs(argv) {
  const args = { dir: null, force: false, help: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--dir') args.dir = argv[++i];
    else if (a === '--force' || a === '-f') args.force = true;
    else if (a === '--help' || a === '-h') args.help = true;
    else {
      console.error(`Unknown option: ${a}`);
      process.exit(1);
    }
  }
  return args;
}

function detectDirs() {
  const home = os.homedir();
  return CANDIDATES
    .map(([label, rel]) => {
      const abs = path.join(home, rel);
      // The agent config dir existing is a good signal the agent is in use.
      const agentRoot = path.dirname(abs);
      return fs.existsSync(agentRoot) ? { label, abs } : null;
    })
    .filter(Boolean);
}

function ask(question) {
  return new Promise((resolve) => {
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
    });
    rl.question(question, (answer) => {
      rl.close();
      resolve(answer.trim());
    });
  });
}

function copyAsset(src, dest) {
  const stat = fs.lstatSync(src);
  if (stat.isDirectory()) {
    fs.mkdirSync(dest, { recursive: true });
    for (const entry of fs.readdirSync(src)) {
      copyAsset(path.join(src, entry), path.join(dest, entry));
    }
  } else {
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    fs.copyFileSync(src, dest);
  }
}

function install(targetRoot, force) {
  const target = path.join(targetRoot, SKILL_NAME);
  if (fs.existsSync(target)) {
    if (!force) {
      console.error(`✗ Already installed at: ${target}`);
      console.error('  Re-run with --force to overwrite.');
      process.exit(1);
    }
    fs.rmSync(target, { recursive: true, force: true });
  }
  fs.mkdirSync(target, { recursive: true });
  const srcRoot = path.resolve(__dirname, '..');
  for (const asset of ASSETS) {
    copyAsset(path.join(srcRoot, asset), path.join(target, asset));
  }
  return target;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    console.log(
      [
        `Usage: npx ${SKILL_NAME} [--dir <skills-dir>] [--force]`,
        '',
        'Copies the skill into your agent skills directory.',
        '  --dir <path>   Target skills directory (e.g. ~/.claude/skills)',
        '  --force        Overwrite an existing install',
      ].join('\n')
    );
    return;
  }

  let targetRoot = args.dir;
  if (targetRoot) {
    targetRoot = targetRoot.replace(/^~(?=\/|$)/, os.homedir());
  } else {
    const found = detectDirs();
    if (found.length === 0) {
      console.error(
        [
          '✗ No agent skills directory detected.',
          '',
          'Pick yours and re-run with --dir, for example:',
          ...CANDIDATES.map(([, rel]) => `  npx ${SKILL_NAME} --dir ~/${rel}`),
          '',
          '(Any directory works — the skill is just files your agent reads.)',
        ].join('\n')
      );
      process.exit(1);
    }
    if (found.length === 1) {
      targetRoot = found[0].abs;
      console.log(`Detected ${found[0].label}: ${found[0].abs}`);
    } else if (process.stdin.isTTY) {
      console.log('Multiple agents detected:');
      found.forEach((d, i) => console.log(`  ${i + 1}) ${d.label}  ${d.abs}`));
      const answer = await ask(`Install into which? [1-${found.length}] `);
      const idx = parseInt(answer, 10) - 1;
      if (Number.isNaN(idx) || idx < 0 || idx >= found.length) {
        console.error('✗ Invalid selection.');
        process.exit(1);
      }
      targetRoot = found[idx].abs;
    } else {
      console.error(
        [
          '✗ Multiple agents detected — choose one with --dir:',
          ...found.map((d) => `  ${d.label}:  npx ${SKILL_NAME} --dir "${d.abs}"`),
        ].join('\n')
      );
      process.exit(1);
    }
  }

  const target = install(targetRoot, args.force);
  console.log(`✓ Installed ${SKILL_NAME} → ${target}`);
  console.log('');
  console.log('Next: start a new agent session and say something like');
  console.log('  "build me a portfolio site" / 「帮我建一个作品集网站」');
  console.log('The skill auto-invokes. Re-run with --force to update later.');
}

main().catch((err) => {
  console.error(`✗ ${err.message}`);
  process.exit(1);
});
