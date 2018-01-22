import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule }   from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { Routes, RouterModule } from '@angular/router';
import { AllItemsComponent } from "./all-items.component";
import { CreateItemComponent } from "./create-item.component";
import { AppService } from "./app.service";

const routes: Routes = [
    {path: "", component: AllItemsComponent},
    {path: "create", component: CreateItemComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes),
        FormsModule,
        HttpClientModule,
        BrowserModule,
  ],
  declarations: [
    AllItemsComponent,
    CreateItemComponent
    ],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  providers: [
    AppService
    ],
  exports: [RouterModule]
})
export class AppRoutingModule { }
