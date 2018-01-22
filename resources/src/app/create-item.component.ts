import {Component} from "@angular/core";
import {Router} from "@angular/router";
import {AppService} from "./app.service";

@Component({
    templateUrl: "create-item.component.html"
})
export class CreateItemComponent {
    public new_name;
    public new_type;
    public alert_msg:string;

    constructor(private _apps:AppService, private _router:Router) {}

    createItem() {
        if (!this.new_name || !this.new_type) {
            return;
        }
        this._apps.createItem({'name': this.new_name, 'type': this.new_type}).then(ret => {
            if (ret == 0) {
                this._router.navigate(['/']);
            } else {
                this.alert_msg = "Unable to create item";
            }
        })
    }
}
