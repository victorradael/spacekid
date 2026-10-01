export interface FileResult {
  path: string;
  status: 'created' | 'appended' | 'skipped';
}

export function detectAppName(projectRoot: string): string;
export function renderRootAgents(appName: string): string;
export function writeOrSkip(filePath: string, content: string): FileResult;
export function writeOrAppend(filePath: string, content: string): FileResult;
export function scaffold(projectRoot: string, appName?: string): FileResult[];
