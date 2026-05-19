#ifndef UI_OVERVIEW_H
#define UI_OVERVIEW_H

#include <QWidget>

namespace Ui {
class ui_overview;
}

class ui_overview : public QWidget
{
    Q_OBJECT

public:
    explicit ui_overview(QWidget *parent = 0);
    ~ui_overview();

private:
    Ui::ui_overview *ui;
};

#endif // UI_OVERVIEW_H
