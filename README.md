<h1>VMSConsulting</h1>
<p>For the Dependencies see requirements text or you can run the command:</p>
<code> > pip install -r requirements.txt </code>

<h2>Redis server</h2>
<p>Need to be installed on the server machine for the chat app</p>
<p>If you work on linux you can search it on google</p>
<p>Or you can run the server using Docker, where you can run the bellow code to make instance and run it:</p>
<code>docker run --name=redis-devel --publish=6379:6379 --hostname=redis --restart=on-failure --detach redis:latest</code>