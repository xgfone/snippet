package utils

import (
	"io/ioutil"
	"os"
	"path/filepath"
	"strings"
)

const (
	NOT_EXIST = iota
	IS_FILE
	IS_DIR
)

func FileType(name string) uint8 {
	fi, err := os.Stat(name)
	if err == nil {
		if fi.IsDir() {
			return IS_DIR
		}
		return IS_FILE
	}
	if os.IsNotExist(err) {
		return NOT_EXIST
	}
	return IS_FILE
}

func IsExist(filename string) bool {
	if FileType(filename) == NOT_EXIST {
		return false
	}
	return true
}

func IsFile(filename string) bool {
	if FileType(filename) == IS_FILE {
		return true
	}
	return false
}

func IsDir(filename string) bool {
	if FileType(filename) == IS_DIR {
		return true
	}
	return false
}

// 获取指定目录下的所有文件，不进入下一级目录搜索，可以匹配后缀过滤。
func ListDir1(dirPth string, suffix string, includeDir bool) ([]string, error) {
	files := make([]string, 0, 25)

	dir, err := ioutil.ReadDir(dirPth)
	if err != nil {
		return nil, err
	}

	suffix = strings.ToUpper(suffix) // 忽略后缀匹配的大小写
	for _, fi := range dir {
		if fi.IsDir() { // 忽略目录
			if includeDir {
				files = append(files, fi.Name())
			}
			continue
		}
		if strings.HasSuffix(strings.ToUpper(fi.Name()), suffix) { // 匹配文件
			files = append(files, fi.Name())
		}
	}

	return files, nil
}

func WalkDirFull(dirPth, suffix string, includeDir, recursion, ignoreError bool) ([]string, error) {
	files := make([]string, 0, 30)
	_, rootDir := filepath.Split(dirPth)

	suffix = strings.ToUpper(suffix)
	err := filepath.Walk(dirPth, func(filename string, fi os.FileInfo, err error) error {
		if err != nil && !ignoreError {
			fmt.Println(err)
			return err
		}

		if fi.IsDir() {
			if fi.Name() == rootDir || recursion {
				return nil
			}

			if includeDir {
				files = append(files, filename)
			}
			fmt.Println(fi.Name())
			return filepath.SkipDir
		}

		if strings.HasSuffix(strings.ToUpper(fi.Name()), suffix) {
			files = append(files, filename)
		}

		return nil
	})

	if err != nil {
		return files, err
	}

	return files, nil
}

func ListDir2(dirPth, suffix string, includeDir bool) ([]string, error) {
	return WalkDirFull(dirPth, suffix, includeDir, false, true)
}

func ListDir(dirPth, suffix string, includeDir bool) ([]string, error) {
	return WalkDirFull(dirPth, suffix, includeDir, false, true)
}

func WalkDir(dirPth, suffix string, recursion bool) ([]string, error) {
	return WalkDirFull(dirPth, suffix, false, recursion, true)
}
