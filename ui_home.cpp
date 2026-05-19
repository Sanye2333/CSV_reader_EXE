#include "ui_home.h"
#include "ui_ui_home.h"

ui_home::ui_home(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::ui_home)
{
    ui->setupUi(this);
}

ui_home::~ui_home()
{
    delete ui;
}
