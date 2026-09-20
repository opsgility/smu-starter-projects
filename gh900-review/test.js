const { shortenUrl, resolveUrl, isValidUrl } = require('./app');

let passed = 0;
let failed = 0;

function test(name, condition) {
    if (condition) {
        console.log(`  PASS: ${name}`);
        passed++;
    } else {
        console.log(`  FAIL: ${name}`);
        failed++;
    }
}

console.log('=== URL Validation Tests ===');
test('Valid HTTPS URL', isValidUrl('https://example.com'));
test('Valid HTTP URL', isValidUrl('http://example.com'));
test('Rejects missing protocol', !isValidUrl('example.com'));
test('Rejects FTP protocol', !isValidUrl('ftp://example.com'));
test('Rejects empty string', !isValidUrl(''));
test('Rejects random text', !isValidUrl('not a url'));

console.log('\n=== Shortening Tests ===');
const result = shortenUrl('https://github.com');
test('Valid URL returns ID', !!result.id);
test('Valid URL returns short URL', !!result.shortUrl);
const invalid = shortenUrl('not-a-url');
test('Invalid URL returns error', !!invalid.error);

console.log('\n=== Resolve Tests ===');
test('Resolves to original URL', resolveUrl(result.id) === 'https://github.com');
test('Unknown ID returns null', resolveUrl('xyz123') === null);

console.log(`\n=== Results: ${passed} passed, ${failed} failed ===`);
process.exit(failed > 0 ? 1 : 0);
