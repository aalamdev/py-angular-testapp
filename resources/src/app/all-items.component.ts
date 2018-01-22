import {Component} from "@angular/core";
import {ModelItem, ModelPermissions} from "./app.models";
import {AppService} from "./app.service";

@Component({
    templateUrl: "all-items.component.html",
    styleUrls: ['all-items.component.css']
})
export class AllItemsComponent {
    public items:ModelItem[];
    public permissions:ModelPermissions;
    public alert_msg:string;

    constructor(private _apps:AppService) {}

    ngOnInit() {
        this._apps.getUserPermissions().then(ret => {
            this.permissions = ret;
        })
        this._apps.getItems({}).then(ret => {
            this.items = ret;
            for (let i of this.items) {
                i['orig_type'] = i['type'];
                i['owner'] = i['owner'];
            }
        });
    }

    updateItem(item:ModelItem) {
        if (item.type == item['orig_type'])
            return

        this._apps.updateItem(item.name, item.type).then(ret => {
            if (ret == 0) {
                item['orig_type'] = item.type;
            } else {
                this.alert_msg = "Unable to update item";
                item.type = item['orig_type'];
            }
        })
    }

    deleteItem(index:number) {
        this._apps.deleteItem(this.items[index].name).then(ret => {
            if (ret == 0) {
                this.items.splice(index, 1);
            } else {
                this.alert_msg = "Unable to delete item"
            }
        })
    }
}
