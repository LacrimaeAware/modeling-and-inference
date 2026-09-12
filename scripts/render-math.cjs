// Render local TeX during the build, including accessible MathML.
const fs = require('node:fs');
const katex = require('../site/vendor/katex/katex.min.js');
const expressions = JSON.parse(fs.readFileSync(0, 'utf8'));
process.stdout.write(JSON.stringify(expressions.map(({tex,display}) =>
  katex.renderToString(tex, {displayMode:display,throwOnError:true,trust:false,output:'htmlAndMathml'})
)));
