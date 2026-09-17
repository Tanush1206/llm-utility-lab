from src.qa import answer_question
from src.summarizer import summarize_text

def main():
    while True:
        print("\n=== LLM Utility Lab ===")
        print("1. Summarize text")
        print("2. Ask a question")
        print("3. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            text = input("\nEnter text to summarize:\n").strip()

            try:
                summary = summarize_text(text)
                print("\n--- Summary ---")
                print(summary.text)

                print("\n---Usage---")
                print(f"Input tokens:, {summary.usage.input_tokens}")
                print(f"Output tokens:, {summary.usage.output_tokens}")
                print(f"Total tokens:, {summary.usage.total_tokens}")

            except (ValueError, RuntimeError) as error:
                print(f"\nError: {error}")

        elif choice == "2":
            context = input("\nEnter context:\n").strip()
            question = input("\nEnter your question:\n").strip()

            try:
                answer = answer_question(context, question)
                print("\n--- Answer ---")
                print(answer.text)

                print("\n---Usage---")
                print(f"Input tokens:, {answer.usage.input_tokens}")
                print(f"Output tokens:, {answer.usage.output_tokens}")
                print(f"Total tokens:, {answer.usage.total_tokens}")
            except (ValueError, RuntimeError) as error:
                print(f"\nError: {error}")

        elif choice == "3":
            print("\nGoodbye! 😄")
            break

        else:
            print("\nInvalid choice. Please select 1,2, or 3.")

if __name__ == "__main__":
    main()
