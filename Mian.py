from GUI import FileServerUI

def main():
    app = FileServerUI(port=8000)
    app.mainloop()

if __name__ == "__main__":
    main()