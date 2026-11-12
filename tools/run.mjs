// npm-independent entry point once the local Node runtime is installed.
import {readFileSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import path from 'node:path';
const config=JSON.parse(readFileSync(new URL('../.runtime/local.json',import.meta.url),'utf8'));
const result=spawnSync(config.node,[config.npm,...process.argv.slice(2)],{stdio:'inherit',env:{...process.env,PATH:path.dirname(config.node)+path.delimiter+(process.env.PATH||'')}});
process.exit(result.status??1);
