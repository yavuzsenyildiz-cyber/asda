import SwiftUI

struct SettingsView: View {
  @EnvironmentObject var viewModel: PCViewModel
  @State private var showBackendURL = false
  @State private var backendURL = ""

  var body: some View {
    NavigationStack {
      List {
        Section("Cihaz Bilgileri") {
          if let device = viewModel.device {
            HStack {
              Text("Ad")
              Spacer()
              Text(device.deviceName)
                .foregroundColor(.gray)
            }

            HStack {
              Text("MAC")
              Spacer()
              Text(device.macAddress)
                .foregroundColor(.gray)
                .font(.caption)
            }
          }
        }

        Section("Sunucu") {
          HStack {
            Text("URL")
            Spacer()
            Text(viewModel.backendURL)
              .foregroundColor(.gray)
              .font(.caption)
          }

          Button("Sunucu Değiştir") {
            showBackendURL = true
          }
        }

        Section("Bilgi") {
          HStack {
            Text("Versiyon")
            Spacer()
            Text("1.0.0")
              .foregroundColor(.gray)
          }
        }

        Section {
          Button(role: .destructive) {
            viewModel.logout()
          } label: {
            Text("Çıkış Yap")
          }
        }
      }
      .navigationTitle("Ayarlar")
      .alert("Sunucu URL", isPresented: $showBackendURL) {
        TextField("URL", text: $backendURL)
        Button("Kaydet") {
          viewModel.backendURL = backendURL
        }
        Button("İptal", role: .cancel) { }
      } message: {
        Text("Arka uç sunucusunun adresini girin")
      }
    }
  }
}

#Preview {
  SettingsView()
    .environmentObject(PCViewModel())
}
