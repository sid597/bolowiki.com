const LANGUAGES = {
  af: 'afrikaans',
  sq: 'albanian',
  am: 'amharic',
  ar: 'arabic',
  hy: 'armenian',
  az: 'azerbaijani',
  eu: 'basque',
  be: 'belarusian',
  bn: 'bengali',
  bs: 'bosnian',
  bg: 'bulgarian',
  ca: 'catalan',
  ceb: 'cebuano',
  ny: 'chichewa',
  'zh-cn': 'chinese (simplified)',
  'zh-tw': 'chinese (traditional)',
  co: 'corsican',
  hr: 'croatian',
  cs: 'czech',
  da: 'danish',
  nl: 'dutch',
  en: 'english',
  eo: 'esperanto',
  et: 'estonian',
  tl: 'filipino',
  fi: 'finnish',
  fr: 'french',
  fy: 'frisian',
  gl: 'galician',
  ka: 'georgian',
  de: 'german',
  el: 'greek',
  gu: 'gujarati',
  ht: 'haitian creole',
  ha: 'hausa',
  haw: 'hawaiian',
  iw: 'hebrew',
  he: 'hebrew',
  hi: 'hindi',
  hmn: 'hmong',
  hu: 'hungarian',
  is: 'icelandic',
  ig: 'igbo',
  id: 'indonesian',
  ga: 'irish',
  it: 'italian',
  ja: 'japanese',
  jw: 'javanese',
  kn: 'kannada',
  kk: 'kazakh',
  km: 'khmer',
  ko: 'korean',
  ku: 'kurdish (kurmanji)',
  ky: 'kyrgyz',
  lo: 'lao',
  la: 'latin',
  lv: 'latvian',
  lt: 'lithuanian',
  lb: 'luxembourgish',
  mk: 'macedonian',
  mg: 'malagasy',
  ms: 'malay',
  ml: 'malayalam',
  mt: 'maltese',
  mi: 'maori',
  mr: 'marathi',
  mn: 'mongolian',
  my: 'myanmar (burmese)',
  ne: 'nepali',
  no: 'norwegian',
  or: 'odia',
  ps: 'pashto',
  fa: 'persian',
  pl: 'polish',
  pt: 'portuguese',
  pa: 'punjabi',
  ro: 'romanian',
  ru: 'russian',
  sm: 'samoan',
  gd: 'scots gaelic',
  sr: 'serbian',
  st: 'sesotho',
  sn: 'shona',
  sd: 'sindhi',
  si: 'sinhala',
  sk: 'slovak',
  sl: 'slovenian',
  so: 'somali',
  es: 'spanish',
  su: 'sundanese',
  sw: 'swahili',
  sv: 'swedish',
  tg: 'tajik',
  ta: 'tamil',
  te: 'telugu',
  th: 'thai',
  tr: 'turkish',
  uk: 'ukrainian',
  ur: 'urdu',
  ug: 'uyghur',
  uz: 'uzbek',
  vi: 'vietnamese',
  cy: 'welsh',
  xh: 'xhosa',
  yi: 'yiddish',
  yo: 'yoruba',
  zu: 'zulu',
};
document.addEventListener('DOMContentLoaded', () => {
  const textareaElement = document.querySelector('.textareaElement');
  const textToTranslate = document.querySelector('#textToTranslate');
  const translatedCardBody = document.querySelector('#translatedCardBody');
  textareaElement.focus();

  // Paste text as plain text in content editable
  document.querySelector('[contenteditable]').addEventListener('paste', (event) => {
    event.preventDefault();
    document.execCommand('inserttext', false, event.clipboardData.getData('text/plain'));
  });

  // Translte the text which is added

  textToTranslate.addEventListener('input', () => {
    // console.log(e);
    const textToTranslateData = textToTranslate.innerHTML;

    const request = new XMLHttpRequest();
    request.open('POST', '/translate/');
    request.onload = () => {
      const responseData = JSON.parse(request.responseText);
      // console.log(` RESPONSE DATA IS : ${responseData.translatedTextResponse}`);
      translatedCardBody.innerHTML = responseData.translatedTextResponse;
    };
    const data = JSON.stringify({ textToTranslate: textToTranslateData, srcLanguage: 'en', destLanguage: 'hi' });
    // console.log(data);
    request.setRequestHeader('Content-type', 'application/json');
    request.send(data);
    // setTimeout(() => {
    //   request.send(data);
    // }, 200);
  });
});
