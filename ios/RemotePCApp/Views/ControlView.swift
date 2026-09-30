import SwiftUI

struct ControlView: View {
  @EnvironmentObject var viewModel: PCViewModel
  @State private var isLoading = false
  @State private var statusMessage = ""
  @State private var showSuccess = false

  var body: some View {
    NavigationStack {
      VStack(spacing: 30) {
        Spacer()

        VStack(spacing: 16) {
          Image(systemName: "power.circle")
            .font(.system(size: 80))
            .foregroundColor(.green)

          Text("Bilgisayarınız")
            .font(.headline)
            .foregroundColor(.gray)

          Text(viewModel.device?.deviceName ?? "Bilinmiyor")
            .font(.title2)
            .fontWeight(.bold)
        }

        Spacer()

        VStack(spacing: 12) {
          Button(action: powerOn) {
            HStack {
              Image(systemName: "power")
              Text("Aç")
            }
            .frame(maxWidth: .infinity)
            .padding()
            .background(Color.green)
            .foregroundColor(.white)
            .cornerRadius(12)
            .font(.headline)
          }
          .disabled(isLoading)

          if !statusMessage.isEmpty {
            Text(statusMessage)
              .font(.caption)
              .foregroundColor(.blue)
              .padding()
              .frame(maxWidth: .infinity)
              .background(Color.blue.opacity(0.1))
              .cornerRadius(8)
          }
        }
        .padding()

        Spacer()
      }
      .navigationTitle("Kontrol")
      .overlay {
        if isLoading {
          ProgressView()
            .scaleEffect(1.5)
        }
      }
      .alert("Başarılı!", isPresented: $showSuccess) {
        Button("Tamam") { }
      } message: {
        Text("Açma komutu gönderildi!")
      }
    }
  }

  private func powerOn() {
    isLoading = true
    statusMessage = "Komut gönderiliyor..."

    viewModel.powerOnPC { success, message in
      isLoading = false
      statusMessage = message ?? ""
      if success {
        showSuccess = true
      }
    }
  }
}

#Preview {
  ControlView()
    .environmentObject(PCViewModel())
}
