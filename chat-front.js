if (!seal.ext.find('spark')) {
  const ext = seal.ext.new('spark', 'Halit', '1.0.0');
  seal.ext.register(ext);
}

let ext = seal.ext.find('spark');
if (!ext) {
  ext = seal.ext.new('spark', 'Halit', '1.0.0');
  seal.ext.register(ext);
}

const cmdChat = seal.ext.newCmdItemInfo();
cmdChat.name = 'c';

cmdChat.solve = async (ctx, msg, cmdArgs) => {
  const prompt = cmdArgs.getArgN(1);
  if (!prompt) {
    seal.replyToSender(ctx, msg, "今天你想和我聊什么呢");
    return seal.ext.newCmdExecuteResult(true);
  }

  // Function to gather non-function properties of an object
  const gatherInfo = (obj) => Object.entries(obj).reduce((acc, [key, value]) => {
    if (typeof value !== 'function') {
      acc[key] = value;
    }
    return acc;
  }, {});

  // Function to extract numeric part of a string
  const extractNumeric = (str) => str.replace(/\D/g, '');

  // Gather group and player information
  const groupInfo = gatherInfo(ctx.group);
  const playerInfo = gatherInfo(ctx.player);

  const requestBody = {
    prompt: prompt,
    groupId: extractNumeric(groupInfo.groupId),
    name: playerInfo.name,
    userId: extractNumeric(playerInfo.userId)
  };

  // Sending data to the backend
  const response = await fetch('http://127.0.0.1:8000/spark/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(requestBody)
  });

  const data = await response.json();
  // Check if the response is a string and parse it if necessary
  let text;
  if (typeof data === 'string') {
    try {
      text = JSON.parse(data).message;
    } catch (error) {
      text = data; // fallback if data is not a JSON string
    }
  } else {
    text = data.message || JSON.stringify(data, null, 2);
  }

  seal.replyToSender(ctx, msg, text);
  return seal.ext.newCmdExecuteResult(true);
};

ext.cmdMap['c'] = cmdChat;