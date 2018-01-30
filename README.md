# Description

A simple test application using python backend and angular frontend.
This is just for illustration purpose for an Aalam cloud developer.


# How to start

- Create the resources folder and installed @angular/cli using
```
npm install @angular/cli
```
- Next create a new angular app using
```
cd resources && ng new --dir .  --routing py-ang-testapp
```

- Modify the src/index.html to have the proper base URL
```
<base href="/aalam/py-ang-testapp"/>
```

- Add the build.sh to build a ahead-of-time compiled app so that it will
be optimized to run faster when loaded.  Notice the build.sh modifies
path of the javascript files to point to the static URL prefix.

- Whenever a change is made to the angular app, run ```./build.sh```. This will
keep the dist folder ready

- Modify the URLs with your own provider code and app code.


# REDIS or MYSQL Database

In app.py, if you set ```USE_REDISDB``` to ```True``` it will use the redis database,
else it will use MYSQL database using sqlalchemy.


# Testing
- To test, you need to setup the SDK as described in this [document](http://docs.aalam.io/_/apps/latest/sdk.html)

- When the SDK is booted, create a provider with your 
[`provider_code`](http://docs.aalam.io/_/apps/latest/definitions.html#provider-code).
In this case, the provider code is `aalam`

- Click on the provider and create an app with the
[`app_code`](http://docs.aalam.io/_/apps/latest/definitions.html#app-code). In this case
it is `pyangtestapp`

- Compress the app's code folder in `.tar.gz` format and submit a new version in the SDK.
This will show how the packaging of the app is being done. This is similar to the packaging
done when you submit it to the [aalam apps server](https://apps.aalam.io/dev)

- After your app is packaged, you have to start the app by clicking on it and
setting it as the current version. 

- Now you can access apps URLs with different user privileges.


# Rebuild the Angular app

To rebuild the angular app, go to the resource folders and first install the 
nodejs packages by executing

```
npm install
```

The above command will take time as it downloads lots of packages. After it
completes, run the 

```
./build.sh
```

from the `resources` folder if you are running linux else

```
build.bat
```

if you are using windows. This will generate the necessary files.

Now you can compress it and submit it in the SDK and verify your changes.
To compress in linux, use this command

```
tar -czf pyangtestapp.tgz example_app/ PKG-INFO resources/ --exclude "resources/node_modules" setup.py
```

In windows you can use the 

```
compress.bat
```

but make sure that you have 7zip install in `C:\Program Files\7zip\`
