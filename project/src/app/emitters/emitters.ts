import { Injectable, EventEmitter } from "@angular/core";

@Injectable({
    providedIn: 'root'
  })
export class Emitters {
    static authEmitter = new EventEmitter<boolean>();
    static activeEmitter = new EventEmitter<boolean>();
}