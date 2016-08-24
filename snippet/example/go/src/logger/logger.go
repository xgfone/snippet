package logger

import (
	"fmt"
	"io"
	"os"

	log "github.com/inconshreveable/log15"
	"github.com/xgfone/go-tools/log/handler"
)

var Logger log.Logger

func init() {
	Logger, _ = NewLogger("info", "")
}

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

func NewLogger(level, filepath string) (logger log.Logger, err error) {
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

	logger = log.New()
	logger.SetHandler(handlers)

	return
}

func Debug(v ...interface{}) {
	Logger.Debug(fmt.Sprint(v...))
}

func Info(v ...interface{}) {
	Logger.Info(fmt.Sprint(v...))
}

func Warn(v ...interface{}) {
	Logger.Warn(fmt.Sprint(v...))
}

func Error(v ...interface{}) {
	Logger.Error(fmt.Sprint(v...))
}

func Crit(v ...interface{}) {
	Logger.Crit(fmt.Sprint(v...))
}

func Debugf(format string, v ...interface{}) {
	Logger.Debug(fmt.Sprintf(format, v...))
}

func Infof(format string, v ...interface{}) {
	Logger.Info(fmt.Sprintf(format, v...))
}

func Warnf(format string, v ...interface{}) {
	Logger.Warn(fmt.Sprintf(format, v...))
}

func Errorf(format string, v ...interface{}) {
	Logger.Error(fmt.Sprintf(format, v...))
}

func Critf(format string, v ...interface{}) {
	Logger.Crit(fmt.Sprintf(format, v...))
}
