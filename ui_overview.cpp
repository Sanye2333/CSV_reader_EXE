#include "ui_overview.h"
#include "ui_ui_overview.h"

ui_overview::ui_overview(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::ui_overview)
{
    ui->setupUi(this);
}

ui_overview::~ui_overview()
{
    delete ui;
}
