
// 2022-CS-31
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
let directoryPath = '';
let outputPath = '';

for (let i = 0; i < args.length; i++) {
    if ((args[i] === '-d' || args[i] === '--directory') && args[i + 1]) {
        directoryPath = args[++i];
    } else if ((args[i] === '-o' || args[i] === '--output') && args[i + 1]) {
        outputPath = args[++i];
    }
}

if (!directoryPath || !outputPath || !fs.existsSync(directoryPath)) {
    console.error("Error: Please provide valid directory and output paths.");
    process.exit(1);
}

const stopWords = new Set(["the", "and", "in", "is", "of", "to", "a", "it", "for", "on", "with"]);

function analyzeFile(filePath) {
    const content = fs.readFileSync(filePath, 'utf8');    
    const lines = content.split(/\r?\n/);
    const words = content.toLowerCase().match(/\b(\w+)\b/g) || [];
    
    let vowels = 0;
    let consonants = 0;
    const wordFreq = {};

    content.toLowerCase().split('').forEach(char => {
        if (/[a-z]/.test(char)) {
            if (/[aeiou]/.test(char)) vowels++;
            else consonants++;
        }        
    });

    words.forEach(word => {
        if (!stopWords.has(word)) {
            wordFreq[word] = (wordFreq[word] || 0) + 1;
        }
    });

    const topWords = Object.entries(wordFreq)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5)
        .map(entry => `${entry[0]} (${entry[1]})`);

    const avgWordLength = words.length > 0 
        ? words.reduce((sum, w) => sum + w.length, 0) / words.length 
        : 0;

    return {
        file: path.basename(filePath),
        lines: lines.length,
        words: words.length,
        top_words: topWords,
        avg_word_length: parseFloat(avgWordLength.toFixed(2)),
        vowel_consonant_ratio: consonants > 0 ? parseFloat((vowels / consonants).toFixed(2)) : vowels
    };
}

const files = fs.readdirSync(directoryPath).filter(f => f.endsWith('.txt'));
const reports = files.map(file => analyzeFile(path.join(directoryPath, file)));

const finalReport = {
    total_files_analyzed: files.length,
    reports: reports
};

fs.writeFileSync(outputPath, JSON.stringify(finalReport, null, 2));