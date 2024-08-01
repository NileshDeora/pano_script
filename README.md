# Extension Project Template

This project was automatically generated.

- `app` - It is a folder link to the location of your *Omniverse Kit* based app.
- `exts` - It is a folder where you can add new extensions. It was automatically added to extension search path. (Extension Manager -> Gear Icon -> Extension Search Path).

Open this folder using Visual Studio Code. It will suggest you to install few extensions that will make python experience better.

Look for "pano_headless" extension in extension manager and enable it. Try applying changes to any python files, it will hot-reload and you can observe results immediately.

Alternatively, you can launch your app from console with this folder added to search path and your extension enabled, e.g.:

```
> app\omni.code.bat --ext-folder exts --enable company.hello.world
```

# App Link Setup

If `app` folder link doesn't exist or broken it can be created again. For better developer experience it is recommended to create a folder link named `app` to the *Omniverse Kit* app installed from *Omniverse Launcher*. Convenience script to use is included.

Run:

```
> link_app.bat
```

If successful you should see `app` folder link in the root of this repo.

If multiple Omniverse apps is installed script will select recommended one. Or you can explicitly pass an app:

```
> link_app.bat --app create
```

You can also just pass a path to create link to:

```
> link_app.bat --path "C:/Users/bob/AppData/Local/ov/pkg/create-2021.3.4"
```


# Sharing Your Extensions

This folder is ready to be pushed to any git repository. Once pushed direct link to a git repository can be added to *Omniverse Kit* extension search paths.

Link might look like this: `git://github.com/[user]/[your_repo].git?branch=main&dir=exts`

Notice `exts` is repo subfolder with extensions. More information can be found in "Git URL as Extension Search Paths" section of developers manual.

To add a link to your *Omniverse Kit* based app go into: Extension Manager -> Gear Icon -> Extension Search Path




# To run command line headless mode
use this command
=> .\app\omni.micro.bat --ext-folder ./exts --enable pano_headless --no-window
To test Api goto 
=> http://localhost:8011/docs

Hit the (Load usd) API Endpoint to load stage before executing the pano generate api
=>output => "Stage loaded."
'GET' \'http://localhost:8011/load_usd' \

To Generate Pano(http://localhost:8011/viewport-capture/make_pano)
Hit with these params=> 

{
  "1": [
    {
      "main_vw": "https://d1g1kk4lk1ysdx.cloudfront.net/wikipoint/image/prev_1514_6785_2_1714486077637.png",
      "other_vw1": "https://d1g1kk4lk1ysdx.cloudfront.net/wikipoint/image/prev_1514_6786_2_1714486788541.png",
      "shop_id" : 1
    },
    {
      "main_vw": "https://d1g1kk4lk1ysdx.cloudfront.net/wikipoint/image/prev_1524_6861_2_1719302956264.png",
      "other_vw1": "https://d1g1kk4lk1ysdx.cloudfront.net/wikipoint/image/prev_1524_6861_2_1719302956264.png",
      "shop_id" : 2
    },
    {
      "main_vw": "https://d1g1kk4lk1ysdx.cloudfront.net/wikipoint/image/prev_1524_6862_2_1719303343962.png",
      "other_vw1": "https://d1g1kk4lk1ysdx.cloudfront.net/wikipoint/image/prev_1524_6862_2_1719303343962.png",
      "shop_id" : 3
    
},
    {
      "main_vw": "https://d1g1kk4lk1ysdx.cloudfront.net/wikipoint/image/prev_1524_6863_2_1719303991858.png",
      "other_vw1": "https://d1g1kk4lk1ysdx.cloudfront.net/wikipoint/image/prev_1524_6863_2_1719303991858.png",
      "shop_id" : 4
    
},
    {
      "main_vw": "https://d1g1kk4lk1ysdx.cloudfront.net/wikipoint/image/prev_1524_6864_2_1719304012209.png",
      "other_vw1": "https://d1g1kk4lk1ysdx.cloudfront.net/wikipoint/image/prev_1524_6864_2_1719304012209.png",
      "shop_id" : 5
    },
    {
      "main_vw": "https://d1g1kk4lk1ysdx.cloudfront.net/wikipoint/image/prev_1524_6865_2_1719304033230.png",
      "other_vw1": "https://d1g1kk4lk1ysdx.cloudfront.net/wikipoint/image/prev_1524_6865_2_1719304033230.png",
      "shop_id" : 6
    }
  ]
}



response will be
Response body
{
  "success": true
}