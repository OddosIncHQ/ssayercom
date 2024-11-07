/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { FormController } from "@web/views/form/form_controller";

class CSVFileParserComponent extends Component {
    setup() {
        super.setup();
        this.displayForm22 = this.props.parsedData && this.props.parsedData.form_section === 'Formulario 22';
        this.displayForm50 = this.props.parsedData && this.props.parsedData.form_section === 'Formulario 50';
        this.displayOtherForms = this.props.parsedData && this.props.parsedData.is_table && !['Formulario 22', 'Formulario 50'].includes(this.props.parsedData.form_section);
    }
}

CSVFileParserComponent.template = 'CSVFileParserComponentTemplate';

// Extending the FormController to add Owl component after form rendering
export class ExtendedFormController extends FormController {
    async willStart() {
        await super.willStart();
        const parsedData = this.model.root.data.parsed_data_ids;
        if (parsedData && parsedData.length > 0) {
            await owl.mount(CSVFileParserComponent, {
                target: this.el.querySelector('.custom-owl-component-container'),
                props: { parsedData },
            });
        }
    }
}

// Register the extended controller
registry.category('controllers').add('extended_form_controller', ExtendedFormController);
