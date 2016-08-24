package logger

import (
	"io"
	"os"

	log "github.com/inconshreveable/log15"
	"github.com/xgfone/go-tools/log/handler"
)

type closingHandler struct {
	io.WriteCloser
	log.Handler
}

func (h *closingHandler) Close() error {
	return h.WriteCloser.Close()
}

func TimedRotatingFileHandler(fmtr log.Format, filename string, backupCount, interval int) (h log.Handler, err error) {
	defer func() {
		if _err := recover(); _err != nil {
			err = _err.(error)
			return
		}
	}()

	_h := handler.NewTimedRotatingFile(filename)
	_h.SetBackupCount(backupCount).SetInterval(interval)

	return closingHandler{_h, log.StreamHandler(_h, fmtr)}, nil
}

type Logger struct {
	log.Logger
}

func NewLogger(level, filepath string) (logger *Logger, err error) {
	// Logger := log.New(os.Stderr, "app", log.LstdFlags|log.Lshortfile)

	var lvl log.Lvl
	if _level, _err := log.LvlFromString(level); _err != nil {
		err = _err
		return
	} else {
		lvl = _level
	}

	var handler log.Handler
	if filepath == "" {
		handler = log.StreamHandler(os.Stderr, log.LogfmtFormat())
	} else {
		handler, err = TimedRotatingFileHandler(log.LogfmtFormat(), filepath, 31, 1)
		// handler, err = log.FileHandler(filepath, log.LogfmtFormat())
		if err != nil {
			return
		}
	}
	// handler = log.SyncHandler(handler)

	//shandler := log.CallerFuncHandler(handler)
	shandler := log.CallerFileHandler(handler)
	chandler := log.CallerStackHandler("%v", handler)

	handlers := log.MultiHandler(
		log.LvlFilterHandler(log.LvlCrit, chandler),
		log.LvlFilterHandler(lvl, shandler),
	)

	_logger := log.New()
	_logger.SetHandler(handlers)

	logger = &Logger{Logger: _logger}

	return
}
