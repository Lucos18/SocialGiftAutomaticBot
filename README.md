<p align="center">
  <img src="https://forthebadge.com/images/badges/made-with-python.svg"/>
  <img src="http://ForTheBadge.com/images/badges/built-by-developers.svg"/>
  <img src="http://ForTheBadge.com/images/badges/uses-git.svg"/>
  <img src="http://ForTheBadge.com/images/badges/built-with-love.svg"/>
</p>


<h2 align="center">👋 Welcome to the future of automation</h2>
<h3 align="center">A simple bot that uses selenium to automate simple actions on Social Gift bot written in Python.</h3>
<h3 align="center">
```
- Use it at your own risk, The administrator of the bot may ban your account (and I would not be responsible for it) -
```
</h3>

<h2 align="center">Installation</h2>
<p align="center">
  <ul>
    <li>Install requirements with the following command : <pre>pip install -r requirements.txt</pre></li>
    <li>Make sure you have Chrome installed</li>
    <li>Install ChromeDriver :<ul>
      <li>Windows :<ul>
        <li>Download Chrome WebDriver : https://chromedriver.chromium.org/downloads</li>
        <li>Place the file in X:\Windows (X as your Windows disk letter)</li>
      </ul>
      <li>MacOS or Linux :<ul>
        <li><pre>apt install chromium-chromedriver</pre></li>
        <li>or if you have brew : <pre>brew cask install chromedriver</pre></li>
      </ul>
    </ul></li>
    <li>Edit the loginCredentials.json.sample with your accounts credentials and rename it by removing .sample at the end.<br/>
  <pre>
    {
        "accountUsername": "Your username",
        "accountPassword": "Your Password"
    }
</pre></li>
	<li>Login to telegram on your chrome browser</li>
	<li>Change inside the python script "pythonbot.py" the arguments to the corresponding one of your computer</li>
    <li>Run the script</li>
   </ul>
</p>

<h2 align="center">Features</h2>
<p align="center">
<ul>
  <li>Creating chromedriver client with auto page loading of the telegram bot </li>
  <li>Auto check if a file is missing and auto creation of it</li>
  <li>Automatic login inside instragram account</li>
  <li>Automatic skip of the ADS</li>
  <li>Counter creation to see how many Likes/Follows/Stories the bot auto completed for you</li>
  <li>Settings file to say what types of campaign the bot need to do and what to skip </li>
</ul>
</p>