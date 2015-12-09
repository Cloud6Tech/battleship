# CST 205
# Final
# utility.py

from javax.swing import JOptionPane

# Display an option dialog with given title (string), message (string), and options (list); returns index of selected option
def getOption(title,message,options):
  return JOptionPane.showOptionDialog(None,message,title,JOptionPane.DEFAULT_OPTION,JOptionPane.QUESTION_MESSAGE,None,options,options[0])