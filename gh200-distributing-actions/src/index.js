const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const count = parseInt(core.getInput('commits') || '10', 10);
    const heading = core.getInput('heading') || 'Changes';

    const token = process.env.GITHUB_TOKEN || core.getInput('github-token');
    const octokit = github.getOctokit(token);
    const { owner, repo } = github.context.repo;

    const { data: commits } = await octokit.rest.repos.listCommits({
      owner,
      repo,
      per_page: count,
    });

    const lines = commits.map(
      (c) => `- ${c.commit.message.split('\n')[0]} (\`${c.sha.slice(0, 7)}\`) — @${c.author?.login || 'unknown'}`
    );

    const notes = `## ${heading}\n\n${lines.join('\n')}\n`;
    core.info(notes);

    core.setOutput('notes', notes);
    core.setOutput('commit-count', String(commits.length));
  } catch (err) {
    core.setFailed(err.message);
  }
}

run();
