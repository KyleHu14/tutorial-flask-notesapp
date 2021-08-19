# Notes on Flask Tutorial : 
# Time Stamp : 25:46
# 1. Template Folder / Templates: 
#   - Templating language is called jinja
#   - Allows you to write a bit of python in your html files


from website import create_app 

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)