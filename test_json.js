
const testStrings = [
    '["computational neuroscience","differential privacy"]',
    '"computational neuroscience"',
    '"differential privacy"',
    '["computational neuroscience", "differential privacy"]' // with space
];

testStrings.forEach(str => {
    try {
        const parsed = JSON.parse(str);
        console.log(`PASS: '${str}' ->`, parsed, `Is Array: ${Array.isArray(parsed)}`);
    } catch (e) {
        console.log(`FAIL: '${str}' -> ${e.message}`);
    }
});
