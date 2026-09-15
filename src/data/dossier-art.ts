export const platoPortrait = {
  src: 'images/plato-silanion-berlin.webp',
  width: 960,
  height: 1335,
  alt: 'Marble portrait of Plato in three-quarter view, his head turned down and left',
  object: 'Plato · Roman copy after a Greek original, 350–340 BCE',
  holdingInstitution: 'Altes Museum, Berlin',
  creator: 'Osama Shukir Muhammed Amin FRCP(Glasg)',
  displayCreator: 'Osama Shukir Muhammed Amin',
  sourceUrl: 'https://commons.wikimedia.org/wiki/File:Marble_bust_of_the_Greek_philosopher_Plato._Roman_copy_(1st_century_CE)_of_an_original_(350-340_BCE)._Altes_Museum,_Berlin.jpg',
  licenseName: 'CC BY-SA 4.0',
  licenseUrl: 'https://creativecommons.org/licenses/by-sa/4.0/',
  adaptation: 'Cropped, WebP-compressed, and CSS-toned to grayscale and sepia.',
} as const

export const platoQuotations = [
  {
    text: 'The many, as we say, are seen but not known, and the ideas are known but not seen.',
    coverExcerpt: 'The many, as we say, are seen but not known.',
    work: 'The Republic',
    locator: 'Book VI · 507b',
    translator: 'Benjamin Jowett',
    sourceUrl: 'https://www.gutenberg.org/ebooks/55201',
  },
  {
    text: 'The beginning is the most important part of any work.',
    work: 'The Republic',
    locator: 'Book II · 377b',
    translator: 'Benjamin Jowett',
    sourceUrl: 'https://www.gutenberg.org/ebooks/55201',
  },
  {
    text: 'Beauty of style and harmony and grace and good rhythm depend on simplicity.',
    work: 'The Republic',
    locator: 'Book III · 400e',
    translator: 'Benjamin Jowett',
    sourceUrl: 'https://www.gutenberg.org/ebooks/55201',
  },
  {
    text: 'Knowledge which is acquired under compulsion obtains no hold on the mind.',
    work: 'The Republic',
    locator: 'Book VII · 536e',
    translator: 'Benjamin Jowett',
    sourceUrl: 'https://www.gutenberg.org/ebooks/55201',
  },
  {
    text: 'The unexamined life is not worth living.',
    work: 'Apology',
    locator: '38a',
    translator: 'Benjamin Jowett',
    sourceUrl: 'https://www.gutenberg.org/ebooks/1656',
  },
] as const

export const dossierCoverQuote = platoQuotations[0]
