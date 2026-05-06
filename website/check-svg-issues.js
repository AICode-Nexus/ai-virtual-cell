#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// 查找所有HTML文件
const htmlFiles = [
  'index.html',
  'component-mapping.html',
  'mapping.html',
  'innovations.html',
  'docs.html',
  'roadmap.html',
  'all-mappings.html'
];

const issues = [];

htmlFiles.forEach(filename => {
  const filePath = path.join(__dirname, filename);

  if (!fs.existsSync(filePath)) {
    console.log(`⚠️  文件不存在: ${filename}`);
    return;
  }

  const content = fs.readFileSync(filePath, 'utf-8');
  const lines = content.split('\n');

  lines.forEach((line, index) => {
    const lineNum = index + 1;

    // 检查1: 旧的 stroke-dasharray="5,5" 模式
    if (line.includes('stroke-dasharray="5,5"')) {
      issues.push({
        file: filename,
        line: lineNum,
        type: 'OLD_DASHARRAY',
        content: line.trim().substring(0, 100)
      });
    }

    // 检查2: SVG元素缺少class属性（应该有语义化类名）
    const svgElementPattern = /<(ellipse|circle|rect|path)\s+(?!.*class=)[^>]*>/;
    if (svgElementPattern.test(line) && line.includes('data-')) {
      // 有data属性但没有class，可能需要添加
      issues.push({
        file: filename,
        line: lineNum,
        type: 'MISSING_CLASS',
        content: line.trim().substring(0, 100)
      });
    }

    // 检查3: 单引号包裹的属性值
    if (line.match(/<[^>]*\s\w+='[^']*'/)) {
      issues.push({
        file: filename,
        line: lineNum,
        type: 'SINGLE_QUOTES',
        content: line.trim().substring(0, 100)
      });
    }

    // 检查4: 空的class属性
    if (line.includes('class=""')) {
      issues.push({
        file: filename,
        line: lineNum,
        type: 'EMPTY_CLASS',
        content: line.trim().substring(0, 100)
      });
    }

    // 检查5: 双空格在class名中
    const classMatch = line.match(/class="([^"]*)"/);
    if (classMatch && classMatch[1].includes('  ')) {
      issues.push({
        file: filename,
        line: lineNum,
        type: 'DOUBLE_SPACE_CLASS',
        content: line.trim().substring(0, 100)
      });
    }
  });
});

// 输出结果
console.log('\n=== SVG 一致性检查结果 ===\n');

if (issues.length === 0) {
  console.log('✅ 没有发现问题！所有HTML文件的SVG元素都符合规范。\n');
  process.exit(0);
}

console.log(`❌ 发现 ${issues.length} 个问题:\n`);

const groupedIssues = {};
issues.forEach(issue => {
  if (!groupedIssues[issue.type]) {
    groupedIssues[issue.type] = [];
  }
  groupedIssues[issue.type].push(issue);
});

Object.keys(groupedIssues).forEach(type => {
  const typeIssues = groupedIssues[type];
  const typeNames = {
    'OLD_DASHARRAY': '旧的 stroke-dasharray="5,5" 模式',
    'MISSING_CLASS': 'SVG元素缺少语义化class',
    'SINGLE_QUOTES': '使用单引号的属性',
    'EMPTY_CLASS': '空的class属性',
    'DOUBLE_SPACE_CLASS': 'class中有双空格'
  };

  console.log(`\n📋 ${typeNames[type]} (${typeIssues.length}个):`);
  console.log('─'.repeat(80));

  typeIssues.forEach(issue => {
    console.log(`  ${issue.file}:${issue.line}`);
    console.log(`    ${issue.content}`);
  });
});

console.log('\n');
process.exit(1);
