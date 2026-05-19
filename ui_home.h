#ifndef UI_HOME_H
#define UI_HOME_H

#include <QWidget>

namespace Ui {
class ui_home;
}

class ui_home : public QWidget
{
    Q_OBJECT

public:
    explicit ui_home(QWidget *parent = 0);
    ~ui_home();

private:
    Ui::ui_home *ui;
};

#endif // UI_HOME_H
