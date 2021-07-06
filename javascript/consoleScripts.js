// csv keys to union
console.log(
  `

keys


`
    .replace(/\n/g, '')
    .split(',')
    .filter((k) => !!k)
    .map((k) => `'${k}'`)
    .join(',')
);
