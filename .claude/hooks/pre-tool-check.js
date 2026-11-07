const fs = require('fs');

function checkPreTool() {
  let command = process.argv.slice(2).join(' ') || '';

  // If command already provided via arguments, test directly without blocking on stdin
  if (!command) {
    try {
      // Only read if stdin has data or was piped
      const stats = fs.fstatSync(0);
      if (stats.size > 0 || !process.stdin.isTTY) {
        // use readFileSync with try/catch
        const rawInput = fs.readFileSync(0, 'utf8');
        if (rawInput) {
          const parsed = JSON.parse(rawInput);
          if (parsed.tool_input) {
            if (parsed.tool_input.command) {
              command = parsed.tool_input.command;
            }
            if (parsed.tool_input.path || parsed.tool_input.file_path) {
              const filePath = parsed.tool_input.path || parsed.tool_input.file_path;
              if (filePath.includes('quiz-pass') || filePath.includes('.githooks')) {
                console.error('Claude cannot touch quiz-pass or .githooks. Operation denied.');
                process.exit(1);
              }
            }
          }
        }
      }
    } catch (e) {}
  }

  const pushPattern = /\bgit\s+push\b/i;
  const noVerifyPattern = /--no-verify\b/i;
  const commitNoVerifyPattern = /\bgit\s+commit\b[^\n]*\s+-n\b/i;

  if (pushPattern.test(command) || noVerifyPattern.test(command) || commitNoVerifyPattern.test(command)) {
    console.error('Claude cannot run git push or skip git hooks. You run this command yourself.');
    process.exit(1);
  }

  if (command.includes('quiz-pass') || command.includes('.githooks')) {
    console.error('Claude cannot touch quiz-pass or .githooks. Operation denied.');
    process.exit(1);
  }

  process.exit(0);
}

checkPreTool();
