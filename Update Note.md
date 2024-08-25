# Add new activities
1. JSON dir = /tutor/app/json; Upload.
2. Make rephrased hints for new json files; /tutor/app/autogen/generte_rephrased.py
3. IMAGE dir = /tutor/static/iamges; Upload.
4. TOOL dir = /tutor/static/popups; Upload.
5. Update the main page, add buttons for the new activities: /tutor/templates/index2.html; /tutor/template/progress.html; 
- The parameters question-name and value must be the correct names, while the text could be different.

# start the system
1. Start mongoDB: systemctl start mongod
2. run the main script: /var/www/tutor/main.py