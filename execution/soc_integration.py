class SOCIntegration:
    def __init__(self):
        pass

    def execute(self, intent, params):
        if intent == "visual_task":
            app = params.get("app", "")
            content = params.get("content", "")
            if app == "word":
                self.write_summary_in_word(content)
            else:
                print(f"SOC would handle: {params}")

    def write_summary_in_word(self, summary_text):
        try:
            import win32com.client
            word = win32com.client.Dispatch("Word.Application")
            word.Visible = True
            doc = word.Documents.Add()
            selection = word.Selection
            selection.TypeText(summary_text)
            print("Summary written to Word document.")
        except Exception as e:
            print(f"Failed to write summary in Word: {e}")