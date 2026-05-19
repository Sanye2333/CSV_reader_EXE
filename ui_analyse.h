#ifndef UI_ANALYSE_H
#define UI_ANALYSE_H

#include <QWidget>

namespace Ui {
class ui_analyse;
}

class ui_analyse : public QWidget
{
    Q_OBJECT

public:
    explicit ui_analyse(QWidget *parent = 0);
    ~ui_analyse();

private:
    Ui::ui_analyse *ui;
};

#endif // UI_ANALYSE_H
