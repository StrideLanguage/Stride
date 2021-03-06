
QT += core gui #qml quick
CONFIG += c++11

lessThan(QT_MAJOR_VERSION, 5): error("Qt 5 required!")
lessThan(QT_MINOR_VERSION, 4): error("Qt 5.4 required!")

QT += webenginewidgets


include(../config.pri)

TARGET = StrideIDE
TEMPLATE = app

SOURCES += main.cpp\
    projectwindow.cpp \
    codeeditor.cpp \
    languagehighlighter.cpp \
#    xmosproject.cpp \
#    platform.cpp
    linenumberarea.cpp \
    configdialog.cpp \
    savechangeddialog.cpp \
    errormarker.cpp \
    searchwidget.cpp \
    tooltip.cpp \
    codemodel.cpp \
    autocompletemenu.cpp

HEADERS  += \
    projectwindow.h \
    codeeditor.h \
    languagehighlighter.h \
#    xmosproject.h \
#    platform.h
    linenumberarea.h \
    configdialog.h \
    savechangeddialog.h \
    errormarker.h \
    searchwidget.h \
    tooltip.hpp \
    codemodel.hpp \
    autocompletemenu.hpp

FORMS    += \
    projectwindow.ui \
    configdialog.ui \
    savechangeddialog.ui \
    searchwidget.ui

# Link to parser library
win32-msvc2015:CONFIG(release, debug|release): LIBS += -L$$OUT_PWD/../parser/release/ -lStrideParser
else:win32-msvc2015:CONFIG(debug, debug|release): LIBS += -L$$OUT_PWD/../parser/debug/ -lStrideParser
else:unix: LIBS += -L$$OUT_PWD/../parser/ -lStrideParser

INCLUDEPATH += $$PWD/../parser
DEPENDPATH += $$PWD/../parser

win32-msvc2015:CONFIG(release, debug|release): PRE_TARGETDEPS += $$OUT_PWD/../parser/release/StrideParser.lib
else:win32-msvc2015:CONFIG(debug, debug|release): PRE_TARGETDEPS += $$OUT_PWD/../parser/debug/StrideParser.lib
else:unix: PRE_TARGETDEPS += $$OUT_PWD/../parser/libStrideParser.a


OTHER_FILES += \
    qml/Editor.qml

RESOURCES += \
    qmlfiles.qrc

win32-msvc2015:CONFIG(release, debug|release): LIBS += -L$$OUT_PWD/../codegen/release/ -lcodegen
else:win32-msvc2015:CONFIG(debug, debug|release): LIBS += -L$$OUT_PWD/../codegen/debug/ -lcodegen
else:unix: LIBS += -L$$OUT_PWD/../codegen/ -lcodegen

INCLUDEPATH += $$PWD/../codegen
DEPENDPATH += $$PWD/../codegen

win32-msvc2015:CONFIG(release, debug|release): PRE_TARGETDEPS += $$OUT_PWD/../codegen/release/codegen.lib
else:win32-msvc2015:CONFIG(debug, debug|release): PRE_TARGETDEPS += $$OUT_PWD/../codegen/debug/codegen.lib
else:unix: PRE_TARGETDEPS += $$OUT_PWD/../codegen/libcodegen.a

win32-msvc2015:CONFIG(release, debug|release): LIBS += -L$$OUT_PWD/../parser/release/ -lStrideParser
else:win32-msvc2015:CONFIG(debug, debug|release): LIBS += -L$$OUT_PWD/../parser/debug/ -lStrideParser
else:unix: LIBS += -L$$OUT_PWD/../parser/ -lStrideParser

INCLUDEPATH += $$PWD/../parser
DEPENDPATH += $$PWD/../parser

win32-msvc2015:CONFIG(release, debug|release): PRE_TARGETDEPS += $$OUT_PWD/../parser/release/StrideParser.lib
else:win32-msvc2015:CONFIG(debug, debug|release): PRE_TARGETDEPS += $$OUT_PWD/../parser/debug/StrideParser.lib
else:unix: PRE_TARGETDEPS += $$OUT_PWD/../parser/libStrideParser.a
