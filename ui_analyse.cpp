#include "ui_analyse.h"
#include "ui_ui_analyse.h"

ui_analyse::ui_analyse(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::ui_analyse)
{
    ui->setupUi(this);
}

ui_analyse::~ui_analyse()
{
    delete ui;
}
