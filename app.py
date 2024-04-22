# Importacoes

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
import logging
from google_sheets_api import GoogleSheets

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

# Constants responsible for being conversation entry points
CHOOSE_OPTION, REGISTER_INCOME_STEP_1, REGISTER_INCOME_STEP_2, REGISTER_INCOME_STEP_3, AWAITING_COMMENT, COMPLETE_INCOME, REGISTER_OUTCOME_STEP_1, REGISTER_OUTCOME_STEP_2, REGISTER_OUTCOME_STEP_3, REGISTER_OUTCOME_STEP_4, COMPLETE_OUTCOME, REGISTER_TRANSFER_STEP_1, REGISTER_TRANSFER_STEP_2, REGISTER_TRANSFER_STEP_3, REGISTER_TRANSFER_STEP_4, COMPLETE_TRANSFER, DISPLAY_REPORT_STEP_1 = range(
    17)


# States(Functions responsible for doing something, called by the state controller)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [["Incomes", "Outcomes", "Transfers", 'Report']]

    await update.message.reply_text(
        "Hi! Choose an option.", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return CHOOSE_OPTION


async def register_income_step_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    await update.message.reply_text("Which input do you want to register?", reply_markup=ReplyKeyboardMarkup(
        [['Salary', '13º Salary', 'Others']], one_time_keyboard=True))

    return REGISTER_INCOME_STEP_1


async def register_income_step_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['category'] = update.message.text

    await update.message.reply_text("Which was the value of the input?", reply_markup=ReplyKeyboardRemove())

    return REGISTER_INCOME_STEP_2


async def register_income_step_3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['value'] = update.message.text

    # Request the comment and wait for the answer
    await update.message.reply_text("Leave a comment?", reply_markup=ReplyKeyboardMarkup([['Yes', 'No']], one_time_keyboard=True))

    return REGISTER_INCOME_STEP_3


async def register_income_step_4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    answer = update.message.text
    if answer == 'Yes':
        await update.message.reply_text("Leave a comment!", reply_markup=ReplyKeyboardRemove())
        return AWAITING_COMMENT  # New state to wait for the comment
    else:
        await update.effective_chat.send_message("Proceeding", reply_markup=ReplyKeyboardRemove())
        # Set the comment as empty if the user doesn't want to add one
        context.user_data['comments'] = ""
        return await complete_income(update, context)


async def awaiting_comment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['comments'] = update.message.text
    return await complete_income(update, context)


async def complete_income(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        category = context.user_data.get('category')
        value = context.user_data.get('value')
        comments = context.user_data.get('comments', '')

        google_sheets_api = GoogleSheets()
        google_sheets_api.insert_incomes(value, category, comments)

        await update.message.reply_text("Entry completed!")
    except Exception as error:
        await update.message.reply_text(f"An error occurred: {error}")
        print(error)
    return ConversationHandler.END


async def register_outcome_step_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Select the type of outcome", reply_markup=ReplyKeyboardMarkup([["Fixed", "Variable"], ["Unique"]], one_time_keyboard=True))

    return REGISTER_OUTCOME_STEP_1


async def register_outcome_step_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['classification'] = update.message.text
    await update.message.reply_text("What is the outcome category?", reply_markup=ReplyKeyboardMarkup([["Bills", "Maintenance", "Subscriptions", "Health"]], one_time_keyboard=True))

    return REGISTER_OUTCOME_STEP_2


async def register_outcome_step_3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['outcome_category'] = update.message.text
    await update.message.reply_text("What was the outcome value?", reply_markup=ReplyKeyboardRemove())

    return REGISTER_OUTCOME_STEP_3


async def register_outcome_step_4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['outcome_value'] = update.message.text
    await update.message.reply_text("Would you like to add a comment?", reply_markup=ReplyKeyboardMarkup([["Yes", "No"]], one_time_keyboard=True))

    return REGISTER_OUTCOME_STEP_4


async def register_outcome_step_5(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    response = update.message.text
    if response == 'Yes':
        await update.message.reply_text("Enter the comment", reply_markup=ReplyKeyboardRemove())
        return COMPLETE_OUTCOME
    else:
        await update.effective_chat.send_message("Ok, proceeding without comments", reply_markup=ReplyKeyboardRemove())

    return await complete_outcome(update, context)


async def complete_outcome(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        context.user_data['comment'] = update.message.text
        print(context.user_data['classification'])
        print(context.user_data['outcome_category'])
        print(context.user_data['outcome_value'])
        print(context.user_data['comment'])

        value = context.user_data['outcome_value']
        classification = context.user_data['classification']
        category = context.user_data['outcome_category']
        comment = context.user_data['comment']

        google_sheets_api = GoogleSheets()
        google_sheets_api.insert_outcomes(
            value, classification, category, comment)

    except Exception as e:
        print('a comment was not provided')

    await update.message.reply_text("Outcome recorded successfully!", reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


async def register_transfer_step_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Which account are you transferring to?", reply_markup=ReplyKeyboardMarkup([["Account 1", "Account 2", "Account 3"]], one_time_keyboard=True))

    return REGISTER_TRANSFER_STEP_1


async def register_transfer_step_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['from_account'] = update.message.text
    await update.message.reply_text("To which account are you transferring?", reply_markup=ReplyKeyboardMarkup([["Account 1", "Account 2", "Account 3"]], one_time_keyboard=True))

    return REGISTER_TRANSFER_STEP_2


async def register_transfer_step_3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['to_account'] = update.message.text
    await update.message.reply_text("What is the transfer amount?", reply_markup=ReplyKeyboardRemove())
    context.user_data['transfer_value'] = update.message.text
    return REGISTER_TRANSFER_STEP_3


async def register_transfer_step_4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['transfer_amount'] = update.message.text
    await update.message.reply_text("Would you like to add a comment?", reply_markup=ReplyKeyboardMarkup([["Yes", "No"]], one_time_keyboard=True))

    return REGISTER_TRANSFER_STEP_4


async def register_transfer_step_5(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    response = update.message.text
    if response == 'Yes':
        await update.message.reply_text("Enter the comment", reply_markup=ReplyKeyboardRemove())
        return COMPLETE_TRANSFER
    else:
        await update.effective_chat.send_message("Ok, proceeding without comments", reply_markup=ReplyKeyboardRemove())

    return await complete_transfer(update, context)


async def complete_transfer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        context.user_data['comment'] = update.message.text
        print(context.user_data['from_account'])
        print(context.user_data['to_account'])
        print(context.user_data['transfer_value'])
        print(context.user_data['comment'])

        from_account = context.user_data['from_account']
        to_account = context.user_data['to_account']
        value = context.user_data['transfer_value']
        comments = context.user_data['comment']

        google_sheets_api = GoogleSheets()
        google_sheets_api.insert_transfers(
            value, from_account, to_account, comments)

    except Exception as e:
        print('a comment was not provided')

    await update.message.reply_text("Transfer registered successfully!", reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


async def display_report_step_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Select the period", reply_markup=ReplyKeyboardMarkup([["Total Incomes", "Total Outcomes", "Total Transfers"]], one_time_keyboard=True))
    return DISPLAY_REPORT_STEP_1


async def display_report_step_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['period'] = update.message.text
    await update.effective_chat.send_message('Ok, proceeding with the report', reply_markup=ReplyKeyboardRemove())
    return await show_report(update, context)


async def show_report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    google_sheet_api = GoogleSheets()
    column = update.message.text
    values = google_sheet_api.show_report(column)
    await update.effective_chat.send_message(f"Your {column} were {values}.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


async def invalid_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("This is not a typing area please restart /start")


def main():
    application = Application.builder().token(
        '6629668965:AAEINdUidQT5stzxVc2v5YfjStTVLJ2HCpM').build()
    conversation_handler = ConversationHandler(
        # entry_points what the person needs to type to start chatting with my bot ex: /start
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSE_OPTION: [
                MessageHandler(filters.Regex("^(Incomes)$"),
                               register_income_step_1),
                MessageHandler(filters.Regex("^(Outcomes)$"),
                               register_outcome_step_1),
                MessageHandler(filters.Regex("^(Transfers)$"),
                               register_transfer_step_1),
                MessageHandler(filters.Regex("^(Report)$"),
                               display_report_step_1),
                MessageHandler(filters.TEXT & ~filters.COMMAND, invalid_input),
            ],
            REGISTER_INCOME_STEP_1: [
                MessageHandler(filters.Regex(
                    "^(Salary|13º Salary|Others)$"), register_income_step_2),
                MessageHandler(filters.TEXT & ~filters.COMMAND, invalid_input),
            ],

            REGISTER_INCOME_STEP_2: [
                MessageHandler(filters.TEXT & ~filters.COMMAND,
                               register_income_step_3)
            ],
            REGISTER_INCOME_STEP_3: [
                MessageHandler(filters.Regex("^(Yes|No)$"),
                               register_income_step_4),
                MessageHandler(filters.TEXT & ~filters.COMMAND, invalid_input)
            ],
            AWAITING_COMMENT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND,
                               awaiting_comment)
            ],
            COMPLETE_INCOME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND,
                               complete_income)
            ],

            REGISTER_OUTCOME_STEP_1: [
                MessageHandler(filters.Regex(
                    "^(Fixed|Variable|Unique)$"), register_outcome_step_2),
                MessageHandler(filters.TEXT & ~filters.COMMAND, invalid_input)
            ],
            REGISTER_OUTCOME_STEP_2: [
                MessageHandler(filters.Regex(
                    "^(Bills|Maintenance|Subscriptions|Health)$"), register_outcome_step_3),
                MessageHandler(filters.TEXT & ~filters.COMMAND, invalid_input)
            ],
            REGISTER_OUTCOME_STEP_3: [
                MessageHandler(filters.TEXT & ~filters.COMMAND,
                               register_outcome_step_4),
            ],
            REGISTER_OUTCOME_STEP_4: [
                MessageHandler(filters.Regex(
                    "^(Yes|No)$"), register_outcome_step_5),
                MessageHandler(filters.TEXT & ~filters.COMMAND, invalid_input)
            ],
            COMPLETE_OUTCOME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND,
                               complete_outcome),
            ],

            REGISTER_TRANSFER_STEP_1: [
                MessageHandler(filters.Regex(
                    "^(Account 1|Account 2|Account 3)$"), register_transfer_step_2),
                MessageHandler(filters.TEXT & ~filters.COMMAND, invalid_input)
            ],

            REGISTER_TRANSFER_STEP_2: [
                MessageHandler(filters.Regex(
                    "^(Account 1|Account 2|Account 3)$"), register_transfer_step_3),
                MessageHandler(filters.TEXT & ~filters.COMMAND, invalid_input)
            ],

            REGISTER_TRANSFER_STEP_3: [
                MessageHandler(filters.TEXT & ~filters.COMMAND,
                               register_transfer_step_4)
            ],

            REGISTER_TRANSFER_STEP_4: [
                MessageHandler(filters.Regex("^(Yes|No)$"),
                               register_transfer_step_5),
                MessageHandler(filters.TEXT & ~filters.COMMAND, invalid_input),
            ],

            COMPLETE_TRANSFER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND,
                               complete_transfer)
            ],

            DISPLAY_REPORT_STEP_1: [
                MessageHandler(filters.Regex("^(Total Incomes|Total Outcomes|Total Transfers)$"),
                               display_report_step_2),
                MessageHandler(filters.TEXT & ~filters.COMMAND, invalid_input)
            ],

        },
        fallbacks=[CommandHandler("start", start)],
    )
    application.add_handler(conversation_handler)
    application.run_polling()


if __name__ == "__main__":
    main()
