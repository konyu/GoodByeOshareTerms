chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if( request.message === "start" ) {
      replace(request.dic);
    }
  }
);

const scanKatakaraWord = (text, dic) => {
  const reg = new RegExp(/[ァ-ンヴー]+/);
  let tmpStr = ""
  let rtnStr = ""
  const len = text.length
  for (let i =0; i < len; i++) {
    if(reg.test(text[i])){
      tmpStr += text[i]
    } else {
      rtnStr += text[i]
    }

  if((i + 1 ) >= len || !reg.test(text[i +1]) ) {
    if(tmpStr.length > 0 ){
      const changedWord = checkDic(tmpStr, dic, 5, 3)
      if( changedWord === null){
        rtnStr += tmpStr
      } else {
        rtnStr += changedWord
      }
      tmpStr = ""
    }
  }
}
return rtnStr
}

const checkDic = (word, dic, index, min) => {
  if(index < min || word.length < min){
    return word
  }
  const changedWholeWord = checkOneWordDic(word, dic)
  if( changedWholeWord !== null){
    return changedWholeWord
  }

  const back = word.substr( - index )
  const forward = word.substr(0,word.length - index )
 
  let rtnStr = ""
  const changedWord = checkOneWordDic(back, dic)
  if( changedWord === null){
    return checkDic(word, dic, index -1, min)
  } else {
    const changedFrontWord = checkOneWordDic(forward, dic)
    if( changedFrontWord === null){
      rtnStr += forward + changedWord
    } else {
      rtnStr += changedFrontWord + changedWord
    }
    return rtnStr
  }  
}

const checkOneWordDic = (word, dic) => {
  const changedWord = dic[word]
      if(changedWord !== undefined){
        // TODO: Debug modeでconsole.logを出力する
        console.log("\"" + word + "\"を\"" + changedWord + "\"に変換")
        return changedWord
      } else {
        return null
      }
}

const replaceText = (node, dic) => {
  const nodeIterator = document.createNodeIterator(node,NodeFilter.SHOW_TEXT)
  let currentNode

  while (currentNode = nodeIterator.nextNode()) {
    currentNode.textContent = scanKatakaraWord(currentNode.textContent, dic) 
  }
}

const replace = (dic) => {
  replaceText(document.body, dic);
  alert("おしゃれワードとさよならしました");
}
