@echo off
set EXIT=f
goto :while1

:while1 (
	IF %EXIT%==t (
		pause
		exit
	) 
	set /p "id=Enter Start Option (Options: sort, ocr, summarize, locator, all): "
    IF %id%==sort (
        python %~dp0\Code\ArchiveAide\main.py -clp
		set EXIT=t
        goto :while1
    ) ELSE (
		IF %id%==ocr (
			python %~dp0\Code\ArchiveAide\main.py -ocr
			set EXIT=t
			goto :while1
		) ELSE (
			IF %id%==summarize (
				python %~dp0\Code\ArchiveAide\main.py -tsa
				set EXIT=t
				goto :while1
			) ELSE (
				IF %id%==all (
					python %~dp0\Code\ArchiveAide\main.py -clp -ocr -tsa -loc
					set EXIT=t
					goto :while1
				) ELSE (
					IF %id%==locator (
						python %~dp0\Code\ArchiveAide\main.py -loc
						set EXIT=t
						goto :while1
					) ELSE (
						goto :while1
					)
				)
			)
		)
	)
)