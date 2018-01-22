#!/bin/bash

ng build  --target=production --environment=prod --aot

for f in `ls dist`; do
    if [ "${f: -3}" == ".js" ]; then
        echo "Compressing $f"
        gzip -c dist/$f > dist/$f.gz
    fi
done

sed -i -e "s#href=\"styles#href=\"/aalam/py_ang_testapp/s/dist/styles#" dist/index.html
sed -i -e "s#src=\"main#src=\"/aalam/py_ang_testapp/s/dist/main#" dist/index.html
sed -i -e "s#src=\"inline#src=\"/aalam/py_ang_testapp/s/dist/inline#" dist/index.html
sed -i -e "s#src=\"vendor#src=\"/aalam/py_ang_testapp/s/dist/vendor#" dist/index.html
sed -i -e "s#src=\"polyfills#src=\"/aalam/py_ang_testapp/s/dist/polyfills#" dist/index.html
ln -sf dist/index.html index.html
