export default {
  async fetch(request, env) {
    if (request.method !== "POST") {
      return new Response("PayP2P Bot is running!", { status: 200 });
    }

    try {
      const update = await request.json();

      // Telegram message / command
      if (update.message) {
        const message = update.message;
        const chatId = message.chat.id;
        const text = message.text || "";

        if (text === "/start") {
          await sendMessage(env.BOT_TOKEN, chatId, homeText(), homeKeyboard());
        }
      }

      // Telegram inline keyboard button
      if (update.callback_query) {
        const query = update.callback_query;
        const chatId = query.message.chat.id;
        const messageId = query.message.message_id;
        const data = query.data;
        const queryId = query.id;

        await answerCallback(env.BOT_TOKEN, queryId);

        let result;

        switch (data) {
          case "buy":
            result = {
              text:
                "🟢 *Buy USDT*\n\n" +
                "Currently available payment methods:\n\n" +
                "💳 bKash\n" +
                "💳 Nagad\n" +
                "🏦 Bank\n\n" +
                "Choose an option below.",
              keyboard: [
                [{ text: "💵 Buy USDT", callback_data: "buy_usdt" }],
                [{ text: "⬅️ Back", callback_data: "home" }]
              ]
            };
            break;

          case "sell":
            result = {
              text:
                "🔴 *Sell USDT*\n\n" +
                "Create a sell advertisement and receive BDT.\n\n" +
                "⚠️ Real trading/escrow will be added in the next version.",
              keyboard: [
                [{ text: "💵 Sell USDT", callback_data: "sell_usdt" }],
                [{ text: "⬅️ Back", callback_data: "home" }]
              ]
            };
            break;

          case "buy_usdt":
            result = {
              text:
                "💵 *Buy USDT*\n\n" +
                "No seller advertisements are available yet.\n\n" +
                "Next version will show:\n" +
                "• Seller rate\n" +
                "• Available USDT\n" +
                "• Payment method\n" +
                "• Seller rating\n" +
                "• Buy button",
              keyboard: [[{ text: "⬅️ Back", callback_data: "home" }]]
            };
            break;

          case "sell_usdt":
            result = {
              text:
                "💵 *Sell USDT*\n\n" +
                "Seller advertisement system will be added next.",
              keyboard: [[{ text: "⬅️ Back", callback_data: "home" }]]
            };
            break;

          case "orders":
            result = {
              text:
                "📋 *My Orders*\n\n" +
                "You don't have any orders yet.",
              keyboard: [[{ text: "⬅️ Back", callback_data: "home" }]]
            };
            break;

          case "wallet":
            result = {
              text:
                "💼 *Wallet*\n\n" +
                "USDT Balance: `0.00 USDT`\n" +
                "BDT Balance: `৳0.00`",
              keyboard: [[{ text: "⬅️ Back", callback_data: "home" }]]
            };
            break;

          case "profile": {
            const user = query.from;

            result = {
              text:
                `👤 *Profile*\n\n` +
                `Name: ${escapeMarkdown(user.first_name || "")}\n` +
                `Username: @${user.username || "Not set"}\n` +
                `User ID: \`${user.id}\`\n\n` +
                `Orders: 0\n` +
                `Success Rate: 100%`,
              keyboard: [[{ text: "⬅️ Back", callback_data: "home" }]]
            };
            break;
          }

          case "support":
            result = {
              text:
                "🆘 *PayP2P Support*\n\n" +
                "For help with an order, contact the administrator.",
              keyboard: [[{ text: "⬅️ Back", callback_data: "home" }]]
            };
            break;

          case "home":
            result = {
              text: homeText(),
              keyboard: homeKeyboard()
            };
            break;

          default:
            result = {
              text: homeText(),
              keyboard: homeKeyboard()
            };
        }

        await editMessage(
          env.BOT_TOKEN,
          chatId,
          messageId,
          result.text,
          result.keyboard
        );
      }

      return new Response("OK", { status: 200 });

    } catch (error) {
      console.error(error);
      return new Response("Error", { status: 500 });
    }
  }
};


// =========================
// PayP2P Home
// =========================

function homeText() {
  return (
    "💰 *Welcome to PayP2P*\n\n" +
    "Buy & Sell USDT with BDT.\n" +
    "Fast • Simple • Secure\n\n" +
    "👇 Choose an option:"
  );
}


function homeKeyboard() {
  return [
    [
      { text: "🟢 Buy USDT", callback_data: "buy" },
      { text: "🔴 Sell USDT", callback_data: "sell" }
    ],
    [
      { text: "📋 My Orders", callback_data: "orders" },
      { text: "💼 Wallet", callback_data: "wallet" }
    ],
    [
      { text: "👤 Profile", callback_data: "profile" },
      { text: "🆘 Support", callback_data: "support" }
    ]
  ];
}


// =========================
// Telegram API
// =========================

async function telegram(token, method, data) {
  const response = await fetch(
    `https://api.telegram.org/bot${token}/${method}`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    }
  );

  return response.json();
}


async function sendMessage(token, chatId, text, keyboard) {
  return telegram(token, "sendMessage", {
    chat_id: chatId,
    text: text,
    parse_mode: "Markdown",
    reply_markup: {
      inline_keyboard: keyboard
    }
  });
}


async function editMessage(token, chatId, messageId, text, keyboard) {
  return telegram(token, "editMessageText", {
    chat_id: chatId,
    message_id: messageId,
    text: text,
    parse_mode: "Markdown",
    reply_markup: {
      inline_keyboard: keyboard
    }
  });
}


async function answerCallback(token, callbackQueryId) {
  return telegram(token, "answerCallbackQuery", {
    callback_query_id: callbackQueryId
  });
}


function escapeMarkdown(text) {
  return String(text).replace(/([_*\[\]()~`>#+\-=|{}.!\\])/g, "\\$1");
}
