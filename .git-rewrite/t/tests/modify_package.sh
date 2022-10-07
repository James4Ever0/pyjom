find | grep -E ".py\$" | xargs -iabc sed -i "s/from modules/from pyjom.modules/g" abc
find | grep -E ".py\$" | xargs -iabc sed -i "s/from main/from pyjom.main/g" abc 
find | grep -E ".py\$" | xargs -iabc sed -i "s/from commons/from pyjom.commons/g" abc
find | grep -E ".py\$" | xargs -iabc sed -i "s/from config/from pyjom.config/g" abc
find | grep -E ".py\$" | xargs -iabc sed -i "s/from medialang/from pyjom.medialang/g" abc
find | grep -E ".py\$" | xargs -iabc sed -i "s/from primitives/from pyjom.primitives/g" abc