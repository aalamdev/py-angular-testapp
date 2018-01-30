echo off

CALL ng build  --target=production --environment=prod --aot

node .build.js dist\index.html "href=\"styles" "href=\"/aalam/pyangtestapp/s/dist/styles"

node .build.js dist\index.html "src=\"main" "src=\"/aalam/pyangtestapp/s/dist/main"

node .build.js dist\index.html "src=\"inline" "src=\"/aalam/pyangtestapp/s/dist/inline"

node .build.js dist\index.html "src=\"vendor" "src=\"/aalam/pyangtestapp/s/dist/vendor"

node .build.js dist\index.html "src=\"polyfills" "src=\"/aalam/pyangtestapp/s/dist/polyfills"

copy /Y dist\index.html index.html

echo Done!