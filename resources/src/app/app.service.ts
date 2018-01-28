import {Injectable} from "@angular/core";
import {HttpClient, HttpParams} from "@angular/common/http";
import {ModelPermissions, ModelItem} from "./app.models";

@Injectable()
export class AppService {
    constructor(private http: HttpClient) {}
    getUserPermissions() {
        return new Promise<ModelPermissions>(resolve => {
            this.http.get<ModelPermissions>("/aalam/pyangtestapp/user_permissions").subscribe(data => {
                resolve(data);
            })
        });
    }
    createItem(body:Object) {
        return new Promise<any>(resolve=> {
            this.http.put("/aalam/pyangtestapp/items", body).subscribe(
                data => {resolve(0)},
                err => {resolve(-1)}
            )
        });
    }
    getItems(params:Object) {
        return new Promise<ModelItem[]>(resolve=> {
            let http_params = new HttpParams()
            for (let k of Object.keys(params))
                http_params.set(k, params[k])
            this.http.get<ModelItem[]>("/aalam/pyangtestapp/items", {params: http_params}).subscribe(
                data => {resolve(data)}
            )
        })
    }
    updateItem(item_name:string, new_type:string) {
        return new Promise<any>(resolve => {
            this.http.post("/aalam/pyangtestapp/item/" + item_name, null, {params: {'type': new_type}}).subscribe(
                data => {resolve(0)},
                err => {resolve(-1)}
            );
        })
    }
    deleteItem(item_name:string) {
        return new Promise<any>(resolve => {
            this.http.delete("/aalam/pyangtestapp/item/" + item_name).subscribe(
                data => {resolve(0)},
                err => {resolve(-1)}
            );
        })
    }
}
