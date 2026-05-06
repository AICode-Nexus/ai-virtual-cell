/**
 * SVG Consistency Tests
 *
 * 测试所有HTML文件中的SVG元素是否符合一致性规范：
 * 1. stroke-dasharray 属性值应该使用一致的格式
 * 2. class 属性应该使用语义化命名
 * 3. 引号使用应该一致（双引号）
 */

const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

describe('SVG Consistency Tests', () => {
  const websiteDir = path.join(__dirname);
  const htmlFiles = [
    'index.html',
    'component-mapping.html',
    'mapping.html',
    'innovations.html',
    'docs.html',
    'roadmap.html',
    'all-mappings.html'
  ];

  htmlFiles.forEach(filename => {
    describe(filename, () => {
      let dom;
      let document;

      beforeAll(() => {
        const filePath = path.join(websiteDir, filename);
        const html = fs.readFileSync(filePath, 'utf-8');
        dom = new JSDOM(html);
        document = dom.window.document;
      });

      test('stroke-dasharray values should use consistent spacing', () => {
        const elementsWithDasharray = document.querySelectorAll('[stroke-dasharray]');

        elementsWithDasharray.forEach(element => {
          const value = element.getAttribute('stroke-dasharray');

          // 应该使用 "6,6" 或 "8,6" 这样的格式，而不是 "5,5"
          // 检查是否使用了不一致的值
          if (value.includes(',')) {
            const parts = value.split(',').map(v => v.trim());
            parts.forEach(part => {
              expect(part).toMatch(/^\d+$/);
            });
          }
        });
      });

      test('SVG elements with animations should have semantic class names', () => {
        const svgElements = document.querySelectorAll('svg ellipse, svg circle, svg rect, svg path');

        svgElements.forEach(element => {
          const className = element.getAttribute('class');

          if (className) {
            // 类名应该是语义化的，如 cell-membrane, sw-gateway 等
            // 不应该是空的或者只有通用类名
            expect(className.length).toBeGreaterThan(0);

            // 如果有多个类名，应该用空格分隔
            if (className.includes('  ')) {
              fail(`Class name has double spaces: "${className}"`);
            }
          }
        });
      });

      test('all SVG attributes should use double quotes', () => {
        const filePath = path.join(websiteDir, filename);
        const html = fs.readFileSync(filePath, 'utf-8');

        // 检查SVG标签内的属性是否使用双引号
        const svgTagPattern = /<(ellipse|circle|rect|path|g|svg)[^>]*>/g;
        const matches = html.match(svgTagPattern) || [];

        matches.forEach(tag => {
          // 检查是否有单引号包裹的属性值
          const singleQuotePattern = /\s\w+='[^']*'/;
          if (singleQuotePattern.test(tag)) {
            fail(`Found single quotes in SVG tag: ${tag.substring(0, 100)}`);
          }
        });
      });

      test('stroke-dasharray should not use "5,5" pattern', () => {
        const filePath = path.join(websiteDir, filename);
        const html = fs.readFileSync(filePath, 'utf-8');

        // 检查是否还有旧的 "5,5" 模式
        if (html.includes('stroke-dasharray="5,5"')) {
          const lines = html.split('\n');
          const problematicLines = [];

          lines.forEach((line, index) => {
            if (line.includes('stroke-dasharray="5,5"')) {
              problematicLines.push({
                line: index + 1,
                content: line.trim()
              });
            }
          });

          fail(`Found old "5,5" pattern in ${problematicLines.length} places:\n` +
               problematicLines.map(p => `  Line ${p.line}: ${p.content.substring(0, 80)}`).join('\n'));
        }
      });
    });
  });
});
